import { API_URL } from "@/_components/utils";
import "@/styles/globals.css";
import axios from "axios";
import type { AppProps } from "next/app";
import Head from "next/head";
import { useEffect } from "react";
import { Toaster } from "react-hot-toast";
import { RecoilRoot } from "recoil";

export default function App({ Component, pageProps }: AppProps) {

  useEffect(() => {
    axios.get(`${API_URL}/fetchdata/`)
      .then(res => {
        console.log(":::result", res.data)
      }).catch(err => {
        console.error(err)
      })
  }, [])

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
