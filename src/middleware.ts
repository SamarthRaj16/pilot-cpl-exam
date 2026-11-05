import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  });

  const pathname = request.nextUrl.pathname;
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    // Development or offline mode without Supabase connected
    return response;
  }

  // FAST PATH: Check if any Supabase session cookies exist
  // Avoids a slow remote network handshake on every page/asset request
  const allCookies = request.cookies.getAll();
  const hasAuthToken = allCookies.some(
    (c) => c.name.includes("-auth-token") && c.value && c.value.length > 10
  );

  // If visiting /admin without any auth token, redirect immediately (0ms delay)
  if (pathname.startsWith("/admin") && !hasAuthToken) {
    const redirectUrl = new URL("/auth/login", request.url);
    redirectUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(redirectUrl);
  }

  // If not accessing /admin and has no auth cookies, pass through with zero network latency
  if (!hasAuthToken) {
    return response;
  }

  // Auth tokens present: validate session with Supabase
  try {
    const supabase = createServerClient(supabaseUrl, supabaseAnonKey, {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({ name, value, ...options });
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          });
          response.cookies.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({ name, value: "", ...options });
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          });
          response.cookies.set({ name, value: "", ...options });
        },
      },
    });

    const {
      data: { user },
    } = await supabase.auth.getUser();

    // Protect /admin routes
    if (pathname.startsWith("/admin")) {
      if (!user) {
        const redirectUrl = new URL("/auth/login", request.url);
        redirectUrl.searchParams.set("redirect", pathname);
        return NextResponse.redirect(redirectUrl);
      }

      // Check admin role
      const { data: profile } = await supabase
        .from("profiles")
        .select("role")
        .eq("id", user.id)
        .single();

      if (profile?.role !== "admin") {
        const forbiddenUrl = new URL("/dashboard", request.url);
        forbiddenUrl.searchParams.set("error", "unauthorized_admin_access");
        return NextResponse.redirect(forbiddenUrl);
      }
    }

    // If logged in and visiting /auth/login or /auth/register, redirect to /dashboard
    if ((pathname === "/auth/login" || pathname === "/auth/register") && user) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  } catch {
    // If Supabase is slow or down, fail open to keep dashboard accessible
    return response;
  }

  return response;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|manifest.json|sw.js|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
