import { Card } from '@mantine/core';
import { ReactNode } from 'react';

interface PageWrapperCardProps {
  children: ReactNode;
}

const PageWrapperCard = ({ children }: PageWrapperCardProps) => (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      {children}
    </Card>
  );
export default PageWrapperCard;
