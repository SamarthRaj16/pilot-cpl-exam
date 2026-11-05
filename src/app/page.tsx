import { redirect } from "next/navigation";
import { cookies } from "next/headers";

export default function HomePage() {
  const cookieStore = cookies();
  const allCookies = cookieStore.getAll();
  const hasAuthToken = allCookies.some(
    (c) => c.name.includes("-auth-token") && c.value && c.value.length > 10
  );
  const isGuest = cookieStore.has("cpl_guest_session");

  // If already authenticated or in guest session, go to dashboard
  if (hasAuthToken || isGuest) {
    redirect("/dashboard");
  } else {
    // New visitors see the Pilot Sign In & Registration portal first
    redirect("/auth/login");
  }
}
