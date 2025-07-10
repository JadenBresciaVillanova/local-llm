import NextAuth, { AuthOptions, Session } from "next-auth"; // Import AuthOptions type
import GithubProvider from "next-auth/providers/github";
import GoogleProvider from "next-auth/providers/google";

// Extend the Session type to include accessToken and id
declare module "next-auth" {
  interface Session {
    accessToken?: string;
    user: {
      id?: string | number;
      name?: string | null;
      email?: string | null;
      image?: string | null;
    };
  }
}

// It's best practice to define the options in a separate const
// for type safety and clarity.
export const authOptions: AuthOptions = {
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    // GoogleProvider({
    //   clientId: process.env.GOOGLE_CLIENT_ID!,
    //   clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    // }),
  ],
  // callbacks: {
  //   async jwt({ token, account }) {
  //     if (account) {
  //       token.accessToken = account.access_token;
  //       token.provider = account.provider;
  //     }
  //     return token;
  //   },
  //   async session({ session, token }) {
  //     // It's safer to type the session object
  //     if (session?.user) {
  //       (session as any).accessToken = token.accessToken;
  //       (session as any).provider = token.provider;
  //     }
  //     return session;
  //   },
  // },
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account) {
        token.accessToken = account.access_token; // GitHub's token
        if (profile) {
          token.id = (profile as { id?: string | number }).id; // GitHub's user ID
          token.email = profile.email; // The user's email from the profile
        }
      }
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken as string | undefined;
      session.user.id = token.id as string | number | undefined; // Pass the ID to the session
      // The user's email is already on session.user.email
      return session;
    },
  },
  // You must provide a secret for production and for JWT encryption
  secret: process.env.NEXTAUTH_SECRET,

  // Optional: Add a debug flag to see more detailed logs during development
  debug: process.env.NODE_ENV === 'development',
};

// The default export handles the API requests
export default NextAuth(authOptions);