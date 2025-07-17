// frontend/src/app/models/page.tsx
"use client";

import { MODEL_DATA } from '../../lib/model-data';
import { ModelCard } from '../../components/ModelCard';

export default function ModelsPage() {
    return (
        <div className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Model Library</h1>
            <p className="text-md text-gray-600 mb-8">
                A guide to the models available in this application.
            </p>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:items-start">
                {MODEL_DATA.map((model) => (
                    <ModelCard key={model.id} model={model} />
                ))}
            </div>
        </div>
    );
}