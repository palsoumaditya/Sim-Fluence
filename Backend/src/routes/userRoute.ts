import { Router } from "express";
import { 
  createUser, 
  getUserById, 
  findOrCreateUser, 
  getUserByRedditId,
  updateUserAnalytics,
  getUsersWithAnalytics
} from "../controllers/userController";

const router = Router();

router.post("/", createUser);
router.post("/findOrCreate", findOrCreateUser);
router.get("/:id", getUserById);
router.get("/reddit/:redditId", getUserByRedditId);
router.get("/", getUserById);

// Analytics routes
router.put("/:id/analytics", updateUserAnalytics);
router.get("/analytics/leaderboard", getUsersWithAnalytics);

export default router;
