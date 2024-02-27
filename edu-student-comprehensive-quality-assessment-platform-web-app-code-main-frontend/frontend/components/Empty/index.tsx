import { Center, Image } from '@mantine/core';

export default function Empty(): JSX.Element {
  return (
    <Center h={700} w="100vw">
      <Image h={160} src="/empty.png" />
    </Center>
  );
}
