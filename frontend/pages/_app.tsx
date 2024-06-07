import FixedChatBot from "@/_components/FloatingChatBot";
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
    const fetchData = async () => {
      try {
        const res = await axios.get(`${API_URL}/fetchdata/`);
        localStorage.setItem("details", JSON.stringify(res?.data?.details));
        localStorage.setItem("stock_data", JSON.stringify(res.data));
        localStorage.setItem("last_fetched_time", Date.now().toString());
      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
  }, []);

  return <>
    <RecoilRoot>
      <Head>
        <title>Future Fund</title>
      </Head>
      <Toaster toastOptions={{ duration: 1200 }} />
      <FixedChatBot/>
      <Component {...pageProps} />
    </RecoilRoot>
  </>;
}
