import "@/styles/globals.css";
import type { AppProps } from "next/app";
import { Toaster } from "react-hot-toast";
import { RecoilRoot } from "recoil";
import { Analytics } from '@vercel/analytics/react';

export default function App({ Component, pageProps }: AppProps) {
  return <>
    <RecoilRoot>
      <Toaster toastOptions={{ duration: 1200 }} />
      <Analytics />
      <Component {...pageProps} />
    </RecoilRoot>
  </>;
}
