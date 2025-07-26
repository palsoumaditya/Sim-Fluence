import { prisma } from "../config/prismaClient";
import { Request, Response } from "express";

// create user
export const createUser = async (req: Request, res: Response) => {
  const { 
    name, 
    email, 
    profileImageUrl, 
    redditId, 
    redditUsername,
    followers,
    following,
    averagePostImpressions,
    totalPosts,
    engagementRate,
    averageLikes,
    averageComments,
    averageShares,
    accountAge,
    redditKarma,
    redditAccountAge,
    verified
  } = req.body;
  try {
    const user = await prisma.user.create({
      data: {
        name,
        email,
        profileImageUrl,
        redditId,
        redditUsername,
        followers,
        following,
        averagePostImpressions,
        totalPosts,
        engagementRate,
        averageLikes,
        averageComments,
        averageShares,
        accountAge,
        redditKarma,
        redditAccountAge,
        verified,
        lastActive: new Date(),
      },
    });
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({ error: "Error creating user" });
  }
};

// get user by id
export const getUserById = async (req: Request, res: Response) => {
  const { id } = req.params;
  try {
    const user = await prisma.user.findUnique({
      where: { id },
    });
    if (!user) {
       res.status(404).json({ error: "User not found" });
       return;
      }
    res.status(200).json(user);
  } catch (error) {
    res.status(500).json({ error: "Error fetching user" });
  }
};

// get all user
export const getAllUsers = async (req: Request, res: Response) => {
  try {
    const users = await prisma.user.findMany();
    res.status(200).json(users);
  } catch (error) {
    res.status(500).json({ error: "Error fetching users" });
  }
};

// Find or create user by email or redditId
export const findOrCreateUser = async (req: Request, res: Response) => {
  const { 
    name, 
    email, 
    profileImageUrl, 
    redditId, 
    redditUsername,
    followers,
    following,
    averagePostImpressions,
    totalPosts,
    engagementRate,
    averageLikes,
    averageComments,
    averageShares,
    accountAge,
    redditKarma,
    redditAccountAge,
    verified
  } = req.body;
  try {
    let user = null;
    
    // First try to find by redditId if provided
    if (redditId) {
      user = await prisma.user.findUnique({ 
        where: { redditId } 
      });
    }
    
    // If not found by redditId, try by email
    if (!user && email) {
      user = await prisma.user.findUnique({ 
        where: { email } 
      });
    }
    
    // If user doesn't exist, create new user
    if (!user) {
      user = await prisma.user.create({
        data: { 
          name, 
          email, 
          profileImageUrl, 
          redditId, 
          redditUsername,
          followers,
          following,
          averagePostImpressions,
          totalPosts,
          engagementRate,
          averageLikes,
          averageComments,
          averageShares,
          accountAge,
          redditKarma,
          redditAccountAge,
          verified,
          lastActive: new Date(),
        },
      });
    } else {
      // Update existing user with new information
      user = await prisma.user.update({
        where: { id: user.id },
        data: { 
          name: name || user.name,
          profileImageUrl: profileImageUrl || user.profileImageUrl,
          redditId: redditId || user.redditId,
          redditUsername: redditUsername || user.redditUsername,
          followers: followers !== undefined ? followers : user.followers,
          following: following !== undefined ? following : user.following,
          averagePostImpressions: averagePostImpressions !== undefined ? averagePostImpressions : user.averagePostImpressions,
          totalPosts: totalPosts !== undefined ? totalPosts : user.totalPosts,
          engagementRate: engagementRate !== undefined ? engagementRate : user.engagementRate,
          averageLikes: averageLikes !== undefined ? averageLikes : user.averageLikes,
          averageComments: averageComments !== undefined ? averageComments : user.averageComments,
          averageShares: averageShares !== undefined ? averageShares : user.averageShares,
          accountAge: accountAge !== undefined ? accountAge : user.accountAge,
          redditKarma: redditKarma !== undefined ? redditKarma : user.redditKarma,
          redditAccountAge: redditAccountAge !== undefined ? redditAccountAge : user.redditAccountAge,
          verified: verified !== undefined ? verified : user.verified,
          lastActive: new Date(),
        },
      });
    }
    
    res.status(200).json(user);
  } catch (error) {
    console.error('Error in findOrCreateUser:', error);
    res.status(500).json({ error: "Error finding or creating user" });
  }
};

// Get user by reddit ID
export const getUserByRedditId = async (req: Request, res: Response) => {
  const { redditId } = req.params;
  try {
    const user = await prisma.user.findUnique({
      where: { redditId },
    });
    if (!user) {
      res.status(404).json({ error: "User not found" });
      return;
    }
    res.status(200).json(user);
  } catch (error) {
    res.status(500).json({ error: "Error fetching user" });
  }
};

// Update user analytics
export const updateUserAnalytics = async (req: Request, res: Response) => {
  const { id } = req.params;
  const {
    followers,
    following,
    averagePostImpressions,
    totalPosts,
    engagementRate,
    averageLikes,
    averageComments,
    averageShares,
    accountAge,
    redditKarma,
    redditAccountAge,
    verified
  } = req.body;
  
  try {
    const user = await prisma.user.update({
      where: { id },
      data: {
        followers,
        following,
        averagePostImpressions,
        totalPosts,
        engagementRate,
        averageLikes,
        averageComments,
        averageShares,
        accountAge,
        redditKarma,
        redditAccountAge,
        verified,
        lastActive: new Date(),
      },
    });
    res.status(200).json(user);
  } catch (error) {
    console.error('Error updating user analytics:', error);
    res.status(500).json({ error: "Error updating user analytics" });
  }
};

// Get users with analytics (for leaderboards, etc.)
export const getUsersWithAnalytics = async (req: Request, res: Response) => {
  const { sortBy = 'followers', order = 'desc', limit = 10 } = req.query;
  
  try {
    const users = await prisma.user.findMany({
      where: {
        followers: { gt: 0 }, // Only users with followers
      },
      orderBy: {
        [sortBy as string]: order as 'asc' | 'desc',
      },
      take: Number(limit),
      select: {
        id: true,
        name: true,
        profileImageUrl: true,
        redditUsername: true,
        followers: true,
        following: true,
        averagePostImpressions: true,
        engagementRate: true,
        verified: true,
        lastActive: true,
      },
    });
    res.status(200).json(users);
  } catch (error) {
    console.error('Error fetching users with analytics:', error);
    res.status(500).json({ error: "Error fetching users with analytics" });
  }
};
