import NextApp, { AppProps, AppContext } from 'next/app';
import Head from 'next/head';
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { ModalsProvider } from '@mantine/modals';
import { theme } from '@/theme';
import './_g.css';

export default function App(props: AppProps) {
  const { Component, pageProps } = props;

  return (
    <>
      <Head>
        <title>{process.env.NEXT_PUBLIC_APP_SUB_TITLE}</title>
        <meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width" />
        <link rel="shortcut icon" href="/favicon.svg" />
      </Head>

        <MantineProvider theme={theme} withCssVariables>
          <ModalsProvider labels={{ confirm: 'Submit', cancel: 'Cancel' }}>
            <Component {...pageProps} />
            <Notifications position="top-right" />
          </ModalsProvider>
        </MantineProvider>
    </>
  );
}

App.getInitialProps = async (appContext: AppContext) => {
  const appProps = await NextApp.getInitialProps(appContext);
  return {
    ...appProps,
  };
};
