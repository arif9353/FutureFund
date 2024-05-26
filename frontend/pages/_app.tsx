import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Head from "next/head";
import { Toaster } from "react-hot-toast";
import { RecoilRoot } from "recoil";

export default function App({ Component, pageProps }: AppProps) {
  return <>
    <RecoilRoot>
      <Head>
        <title>Future Fund</title>
      </Head>
      <Toaster toastOptions={{ duration: 1200 }} />
      <Component {...pageProps} />
    </RecoilRoot>
  </>;
}
