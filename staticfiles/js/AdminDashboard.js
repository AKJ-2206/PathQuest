import React, { useState, useEffect } from 'react';
// ... other imports ...

const AdminDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    fetch('/api/admin-dashboard-data/')
      .then(response => response.json())
      .then(data => setDashboardData(data))
      .catch(error => console.error('Error fetching dashboard data:', error));
  }, []);

  if (!dashboardData) return <div>Loading...</div>;

  // Use dashboardData instead of hardcoded values
  const { totalCourses, totalUsers, totalOrders, totalRevenue, dailyRevenue, topCourses, userRegistrations } = dashboardData;

  // ... rest of the component ...
};

export default AdminDashboard;