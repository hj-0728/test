import dayjs from 'dayjs';
import { Box, createStyles, Anchor, Group, Text, useMantineTheme } from '@mantine/core';
import useAppState from '../../../../store/app';

const useStyles = createStyles((theme) => ({
  footer: {
    // marginTop: rem(120),
    position: 'fixed',
    bottom: 0,
    height: 36,
    zIndex: 1000,
    right: 0,
    display: 'flex',
    textAlign: 'center',
    justifyContent: 'center',
    fontSize: 14,
  },

  inner: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: `${theme.spacing.md} ${theme.spacing.md}`,

    [theme.fn.smallerThan('sm')]: {
      flexDirection: 'column',
    },
  },

  links: {
    [theme.fn.smallerThan('sm')]: {
      marginTop: theme.spacing.lg,
      marginBottom: theme.spacing.sm,
    },
  },
}));

interface FooterCenteredProps {
  links: { link: string; label: string }[];
}

const FooterCentered = ({ links }: FooterCenteredProps) => {
  const { classes } = useStyles();
  const { colorScheme, sidebarWidth } = useAppState();
  const { colors } = useMantineTheme();
  const items = links.map((link) => (
    <Anchor<'a'>
      color="dimmed"
      key={link.label}
      href={link.link}
      sx={{ lineHeight: 1 }}
      onClick={(event) => event.preventDefault()}
      size="sm"
    >
      {link.label}
    </Anchor>
  ));

  return (
    <Box
      className={classes.footer}
      sx={{ left: sidebarWidth,
        backgroundColor: colorScheme === 'dark' ? colors.dark[8] : colors.gray[0],
        color: colorScheme === 'dark' ? colors.gray[0] : colors.dark[5] }}
    >
      <div className={classes.inner}>
        <Text> &copy;{dayjs().year()}Next Mantine Dashboard</Text>
        <Group className={classes.links}>{items}</Group>
      </div>
    </Box>
  );
};

export default FooterCentered;
