export const DashboardPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Active Alerts</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">24</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Open Investigations</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">8</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Monitored Users</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">256</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Devices</h3>
          <p className="text-3xl font-bold text-brand-600 mt-2">512</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Alerts</h2>
          <p className="text-gray-600">Placeholder: Alerts chart will be here</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Investigation Timeline</h2>
          <p className="text-gray-600">Placeholder: Timeline chart will be here</p>
        </div>
      </div>
    </div>
  )
}
