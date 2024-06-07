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
      const stockData = localStorage.getItem('stock_data');
      const lastFetchedTime = localStorage.getItem('last_fetched_time');
      const thirtyMinutes = 30 * 60 * 1000; // 30 minutes in milliseconds

      if (stockData && lastFetchedTime) {
        const timeElapsed = Date.now() - parseInt(lastFetchedTime, 10);
        if (timeElapsed < thirtyMinutes) {
          // Data is recent, no need to call the API
          console.log('Using cached data');
          return;
        }
      }

      try {
        const res = await axios.get(`${API_URL}/fetchdata/`);
        console.log(":::result", res.data);
        localStorage.setItem("details", JSON.stringify(res.data));
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
      <Component {...pageProps} />
    </RecoilRoot>
  </>;
}
