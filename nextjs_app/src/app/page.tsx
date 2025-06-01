import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <main className="flex flex-col items-center justify-center min-h-screen p-8">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Daily Planner AI Agent
          </h1>
          <p className="text-xl text-gray-600 mb-8 leading-relaxed">
            Your personal AI chief-of-staff for intelligent task management, 
            daily planning, and productivity optimization. Built for solo founders 
            and build-in-public creators who need an AI that truly gets them.
          </p>
          
          <div className="flex gap-6 justify-center mb-12">
            <Link
              href="/tasks"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
            >
              View Tasks
            </Link>
            <Link
              href="/tasks"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-50 transition-colors border border-blue-200 shadow-lg"
            >
              Get Started
            </Link>
          </div>

          <div className="grid md:grid-cols-3 gap-8 text-left">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🎯</div>
              <h3 className="text-lg font-semibold mb-2">Smart Task Management</h3>
              <p className="text-gray-600">
                Natural language task creation with intelligent prioritization and scheduling.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">🤖</div>
              <h3 className="text-lg font-semibold mb-2">Personalized AI</h3>
              <p className="text-gray-600">
                Adapts to your communication style and motivation patterns for maximum effectiveness.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl mb-4">📅</div>
              <h3 className="text-lg font-semibold mb-2">Dynamic Planning</h3>
              <p className="text-gray-600">
                Real-time schedule adjustments and intelligent conflict resolution.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
