// frontend/src/components/ParameterSliders.tsx
"use client";

import React from 'react';

// Define the shape of the token counts object
interface TokenCounts {
    prompt_tokens: number;
    response_tokens: number;
    total_tokens: number;
}

interface ParameterSlidersProps {
    temperature: number;
    setTemperature: (value: number) => void;
    topP: number;
    setTopP: (value: number) => void;
    maxTokens: number;
    setMaxTokens: (value: number) => void;
    lastTokenCount: TokenCounts | null;
}

// A reusable component for a single slider
const Slider = ({ label, value, min, max, step, onChange }: any) => (
    <div>
        <div className="flex justify-between text-sm mb-1">
            <label className="font-medium text-gray-700">{label}</label>
            <span className="text-gray-500">{value}</span>
        </div>
        <input
            type="range"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={(e) => onChange(parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
    </div>
);

export default function ParameterSliders({ temperature, setTemperature, topP, setTopP, maxTokens, setMaxTokens, lastTokenCount }: ParameterSlidersProps) {
    return (
        <div className="space-y-4">
            <Slider label="Temperature" value={temperature} min={0} max={1} step={0.05} onChange={setTemperature} />
            <Slider label="Top P" value={topP} min={0} max={1} step={0.05} onChange={setTopP} />
            
            <div>
                <div className="flex justify-between text-sm mb-1">
                    <label className="font-medium text-gray-700">Max Response Tokens</label>
                    <span className="text-gray-500">{maxTokens}</span>
                </div>
                <input
                    type="range"
                    min={128}
                    max={8192}
                    step={128}
                    value={maxTokens}
                    onChange={(e) => setMaxTokens(parseInt(e.target.value, 10))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
            </div>
            
            {lastTokenCount && (
                <div className="mt-4 pt-4 border-t border-gray-200 text-xs text-gray-600">
                    <h4 className="font-semibold mb-2 text-center">Last Request Tokens</h4>
                    <div className="flex justify-between"><span>Prompt:</span> <span>{lastTokenCount.prompt_tokens}</span></div>
                    <div className="flex justify-between"><span>Response:</span> <span>{lastTokenCount.response_tokens}</span></div>
                    <div className="flex justify-between font-bold"><span>Total:</span> <span>{lastTokenCount.total_tokens}</span></div>
                </div>
            )}
        </div>
    );
}