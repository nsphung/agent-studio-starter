"use client";

import { CopilotSidebar } from "@copilotkit/react-ui"; 
import { useDefaultTool, useRenderToolCall } from "@copilotkit/react-core";

export default function Page() {
    useDefaultTool({
    render: ({name, status, args, result}) => (
        <details>
            <summary>
                {status === "complete"? `Called ${name}` : `Calling ${name}`}
            </summary>

            <p>Status: {status}</p>
            <p>Args: {JSON.stringify(args)}</p>
            <p>Result: {JSON.stringify(result)}</p>
        </details>
        )
    })
    
    useRenderToolCall({
        name: "get_weather",
        render: ({status, args, result}) => {
            // Parse weather result if available - handle both JSON and plain text
            let weatherData = null;
            try {
                weatherData = result && typeof result === 'string' ? JSON.parse(result) : result;
            } catch (e) {
                // If parsing fails, result is plain text
                weatherData = null;
            }
            
            // Get weather icon based on condition
            const getWeatherIcon = (condition: string) => {
                const conditionLower = condition?.toLowerCase() || '';
                if (conditionLower.includes('sunny') || conditionLower.includes('clear')) return '☀️';
                if (conditionLower.includes('cloud')) return '☁️';
                if (conditionLower.includes('rain')) return '🌧️';
                if (conditionLower.includes('snow')) return '❄️';
                if (conditionLower.includes('thunder') || conditionLower.includes('storm')) return '⛈️';
                if (conditionLower.includes('fog') || conditionLower.includes('mist')) return '🌫️';
                return '🌤️';
            };

            // Get background gradient based on weather
            const getWeatherGradient = (condition: string) => {
                const conditionLower = condition?.toLowerCase() || '';
                if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
                    return 'from-yellow-400 via-orange-400 to-pink-400';
                }
                if (conditionLower.includes('cloud')) {
                    return 'from-gray-400 via-gray-500 to-gray-600';
                }
                if (conditionLower.includes('rain')) {
                    return 'from-blue-400 via-blue-500 to-blue-600';
                }
                if (conditionLower.includes('snow')) {
                    return 'from-blue-200 via-blue-300 to-blue-400';
                }
                return 'from-cyan-400 via-blue-400 to-indigo-500';
            };

            const condition = weatherData?.weather || result || 'sunny';
            
            return (
                <div className="my-4 mx-auto max-w-sm">
                    <div className={`relative overflow-hidden rounded-2xl shadow-2xl bg-gradient-to-br ${getWeatherGradient(condition)} p-6 text-white transition-all duration-300 hover:shadow-3xl hover:scale-105`}>
                        {/* Background decoration */}
                        <div className="absolute top-0 right-0 w-32 h-32 bg-white opacity-10 rounded-full -mr-16 -mt-16"></div>
                        <div className="absolute bottom-0 left-0 w-24 h-24 bg-white opacity-10 rounded-full -ml-12 -mb-12"></div>
                        
                        <div className="relative z-10">
                            {/* Status indicator */}
                            {status !== "complete" && (
                                <div className="flex items-center gap-2 mb-4 animate-pulse">
                                    <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                                    <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                                    <span className="text-sm font-medium ml-2">Fetching weather...</span>
                                </div>
                            )}

                            {/* Location */}
                            <div className="flex items-center justify-between mb-6">
                                <div>
                                    <h3 className="text-2xl font-bold">
                                        {weatherData.location || 'Unknown Location'}
                                    </h3>
                                    <p className="text-sm opacity-90 mt-1">
                                        {status === "complete" ? "Current Weather" : "Loading..."}
                                    </p>
                                </div>
                                <div className="text-6xl">
                                    {getWeatherIcon(condition)}
                                </div>
                            </div>

                            {/* Weather details */}
                            {status === "complete" && weatherData && (
                                <div className="space-y-3">
                                    <div className="flex items-baseline gap-2">
                                        <span className="text-5xl font-bold">
                                            {weatherData.temperature || '25'}°
                                        </span>
                                        <span className="text-xl opacity-80">
                                            {weatherData.unit || 'C'}
                                        </span>
                                    </div>
                                    
                                    <div className="pt-4 border-t border-white/20">
                                        <p className="text-lg font-medium capitalize">
                                            {condition}
                                        </p>
                                        
                                        <div className="grid grid-cols-2 gap-4 mt-4">
                                            {weatherData.humidity && (
                                                <div className="flex items-center gap-2">
                                                    <span className="text-2xl">💧</span>
                                                    <div>
                                                        <p className="text-xs opacity-80">Humidity</p>
                                                        <p className="font-semibold">{weatherData.humidity}%</p>
                                                    </div>
                                                </div>
                                            )}
                                            {weatherData.windSpeed && (
                                                <div className="flex items-center gap-2">
                                                    <span className="text-2xl">💨</span>
                                                    <div>
                                                        <p className="text-xs opacity-80">Wind</p>
                                                        <p className="font-semibold">{weatherData.windSpeed} mph</p>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Simple result display if no structured data */}
                            {status === "complete" && !weatherData && result && (
                                <div className="pt-4 border-t border-white/20">
                                    <p className="text-lg">{result}</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            );
        }   
    })

    return (
        <main>
            <h1>Your App so so good!</h1>
            <CopilotSidebar />
        </main>
    );
}