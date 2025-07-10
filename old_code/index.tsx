// import { useSession, signIn, signOut } from "../../node_modules/next-auth/react";
// import ChatWindow from "../components/ChatWindow"; // Move ChatWindow to a components folder

// export default function Home() {
//   const { data: session, status } = useSession();

//   // Show a loading state while the session is being checked
//   if (status === "loading") {
//     return <p>Loading...</p>;
//   }

//   // If the user is authenticated, show the chat window and a sign-out button
//   if (session) {
//     return (
//       <div>
//         <p>Signed in as {session.user?.email}</p>
//         <button onClick={() => signOut()}>Sign out</button>
//         <hr />
//         <ChatWindow />
//       </div>
//     );
//   }

//   // If the user is not authenticated, show sign-in buttons
//   return (
//     <div>
//       <h1>Welcome! Please sign in.</h1>
//       <button onClick={() => signIn("github")}>Sign in with GitHub</button>
//       <br />
//       {/* <button onClick={() => signIn("google")}>Sign in with Google</button> */}
//     </div>
//   );
// }