import NextAuth from "next-auth";
import RedditProvider from "next-auth/providers/reddit";

export default NextAuth({
  // Configure one or more authentication providers
  providers: [
    RedditProvider({
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET,
    }),
    // ...add more providers here
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      if (account?.provider === "reddit") {
        try {
          // Calculate account age in days
          const accountAge = profile?.created_utc 
            ? Math.floor((Date.now() / 1000 - profile.created_utc) / (24 * 60 * 60))
            : null;

          // Store user details in database with social media analytics
          const response = await fetch(`${process.env.BACKEND_URL}/api/v1/user/findOrCreate`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: user.name || profile?.name,
              email: user.email || `${user.id}@reddit.com`,
              profileImageUrl: user.image,
              redditId: user.id,
              redditUsername: profile?.name,
              // Social media analytics data
              followers: profile?.subreddit?.subscribers || 0,
              following: 0, // Reddit doesn't provide following count in basic profile
              averagePostImpressions: 0, // Will be updated later with actual data
              totalPosts: profile?.num_posts || 0,
              engagementRate: 0.0, // Will be calculated based on actual engagement
              averageLikes: profile?.upvote_ratio ? Math.round(profile.upvote_ratio * 100) : 0,
              averageComments: 0, // Will be updated with actual data
              averageShares: 0, // Reddit doesn't have shares like other platforms
              accountAge: accountAge,
              redditKarma: profile?.total_karma || 0,
              redditAccountAge: accountAge,
              verified: profile?.verified || false,
            }),
          });

          if (!response.ok) {
            console.error('Failed to store user in database:', await response.text());
            return false;
          }

          const userData = await response.json();
          user.databaseId = userData.id;
          return true;
        } catch (error) {
          console.error('Error storing user in database:', error);
          return false;
        }
      }
      return true;
    },
    async jwt({ token, account, user }) {
      // Persist the OAuth access_token to the token right after signin
      if (account) {
        token.accessToken = account.access_token;
      }
      if (user?.databaseId) {
        token.databaseId = user.databaseId;
      }
      return token;
    },
    async session({ session, token }) {
      // Send properties to the client, like an access_token from a provider.
      session.accessToken = token.accessToken;
      session.databaseId = token.databaseId;
      return session;
    },
  },
});