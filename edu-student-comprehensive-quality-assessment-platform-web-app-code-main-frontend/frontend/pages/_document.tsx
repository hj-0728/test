import { Html, Head, Main, NextScript } from 'next/document';
import { ColorSchemeScript } from '@mantine/core';

export default function Document() {
  return (
    <Html lang="zh" style={{ height: '100%' }}>
      <Head>
        <ColorSchemeScript defaultColorScheme="auto" />
      </Head>
      <body style={{ backgroundColor: 'white', height: '100%' }}>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
