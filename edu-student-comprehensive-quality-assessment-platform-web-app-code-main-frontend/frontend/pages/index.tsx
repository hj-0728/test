import { useEffect } from 'react';
import Router from 'next/router';

// import { Welcome } from '../components/Welcome/Welcome';
// import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';

export default function HomePage() {
  useEffect(() => {
    Router.push('/dashboard');
  });
  return (
    <>
    </>
  );
}
