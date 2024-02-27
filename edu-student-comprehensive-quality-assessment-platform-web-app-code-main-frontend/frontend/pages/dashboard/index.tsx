import { NextPage } from 'next';
import { useEffect } from 'react';
import AdminLayout from '../../layouts/adminLayout';

const DashboardPage: NextPage = () => {
  useEffect(() => {
    console.log('Dashboard page mounted');
  });
  return (
    <AdminLayout>
      <h1>Dashboard</h1>
    </AdminLayout>
  );
};

export default DashboardPage;
