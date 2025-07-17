"use client";

import { FC, useState } from 'react'; // Import useState
import { ModelInfo } from '../lib/model-data';
import { 
    FaMemory, FaHdd, FaMicrochip, FaBoxOpen, FaCalendarAlt, 
    FaComments, FaBalanceScale, FaLink, FaCheckCircle, 
    FaTimesCircle, FaTachometerAlt, FaGraduationCap, FaCalculator, FaCode,
    FaChevronDown, FaChevronUp // New icons for the button
} from 'react-icons/fa';

interface ModelCardProps {
  model: ModelInfo;
}

// Helper for sections with bullet points
const InfoSection: FC<{ title: string; items: string[] }> = ({ title, items }) => {
  if (!items || items.length === 0) return null;
  return (
    <div className="mb-6">
      <h4 className="font-semibold text-gray-800 mb-2">{title}</h4>
      <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
        {items.map((item, index) => <li key={index}>{item}</li>)}
      </ul>
    </div>
  );
};

// Helper for key-value info with icons
const KeyInfoItem: FC<{ icon: React.ReactNode; label: string; value: string }> = ({ icon, label, value }) => {
    if (!value) return null;
    return (
        <div className="flex items-center text-sm gap-x-2">
            <span className="text-gray-500">{icon}</span>
            <span className="text-gray-600 whitespace-nowrap">{label}:</span>
            <span className="font-medium text-gray-800 break-words flex-1">{value}</span>
        </div>
    );
};

// Helper for Benchmark Scores
const BenchmarkScores: FC<{ scores: ModelInfo['benchmarks'] }> = ({ scores }) => {
    if (!scores) return null;
    return (
      <div className="mb-6">
        <h4 className="font-semibold text-gray-800 mb-2">Benchmarks</h4>
        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
            <KeyInfoItem icon={<FaTachometerAlt/>} label="MT-Bench" value={scores.mt_bench?.toString() || 'N/A'} />
            <KeyInfoItem icon={<FaGraduationCap/>} label="MMLU" value={scores.mmlu?.toString() || 'N/A'} />
            <KeyInfoItem icon={<FaCalculator/>} label="GSM8K" value={scores.gsm8k?.toString() || 'N/A'} />
            <KeyInfoItem icon={<FaCode/>} label="HumanEval" value={scores.human_eval?.toString() || 'N/A'} />
        </div>
      </div>
    );
}

// Helper for Transparency Info
const TransparencyInfo: FC<{ info: ModelInfo['open_source_transparency'] }> = ({ info }) => (
    <div className="text-sm space-y-2">
        <div className="flex items-center">
            {info.has_weights ? <FaCheckCircle className="text-green-500 mr-2"/> : <FaTimesCircle className="text-red-500 mr-2"/>}
            Weights Available
        </div>
        <div className="flex items-center">
            {info.has_details ? <FaCheckCircle className="text-green-500 mr-2"/> : <FaTimesCircle className="text-red-500 mr-2"/>}
            Training Details Public
        </div>
        {info.link && (
            <a href={info.link} target="_blank" rel="noopener noreferrer" className="flex items-center text-blue-600 hover:underline">
                <FaLink className="mr-2"/> Learn More
            </a>
        )}
    </div>
);

export const ModelCard: FC<ModelCardProps> = ({ model }) => {
  // --- NEW: State to control the expanded view ---
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-200 transition-all duration-300">
      <div className="p-6">
        {/* --- HEADER (Always Visible) --- */}
        <h3 className="text-2xl font-bold text-gray-900">{model.name}</h3>
        <p className="text-md text-gray-600 mt-1">{model.intended_use}</p>
        <div className="mt-4 flex flex-wrap gap-2 text-xs">
            <span className="font-semibold bg-blue-100 text-blue-800 px-2.5 py-1 rounded-full">{model.architecture}</span>
            <span className="font-semibold bg-green-100 text-green-800 px-2.5 py-1 rounded-full">{model.param_count}</span>
            <span className="font-semibold bg-indigo-100 text-indigo-800 px-2.5 py-1 rounded-full">{model.domain_specialization}</span>
            <span className="font-semibold bg-purple-100 text-purple-800 px-2.5 py-1 rounded-full">{model.type}</span>
        </div>
        <p className="mt-5 text-sm text-gray-700 leading-relaxed">{model.summary}</p>
        
        {/* --- INITIAL DETAILS GRID (Always Visible) --- */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
            <div>
                <InfoSection title="Advantages" items={model.advantages} />
            </div>
            <div className="space-y-6">
                <div>
                    <h4 className="font-semibold text-gray-800 mb-2">Key Info</h4>
                    <div className="space-y-2">
                        <KeyInfoItem icon={<FaComments />} label="Dialogue Style" value={model.dialogue_style} />
                        <KeyInfoItem icon={<FaBoxOpen />} label="Context Length" value={model.context_length} />
                        <KeyInfoItem icon={<FaCalendarAlt />} label="Knowledge Cutoff" value={model.knowledge_cutoff} />
                    </div>
                </div>
            </div>
        </div>
        
        {/* --- EXPANDABLE CONTENT --- */}
        <div className={`transition-all duration-500 ease-in-out overflow-hidden ${isExpanded ? 'max-h-[1000px] opacity-100' : 'max-h-0 opacity-0'}`}>
            <div className="pt-6 border-t border-gray-200 mt-1 grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
                {/* Left Column */}
                <div>
                    <InfoSection title="Use Cases" items={model.use_cases} />
                    <InfoSection title="Weaknesses" items={model.weaknesses} />
                    <div>
                            <h4 className="font-semibold text-gray-800 mb-2">Licensing & Openness</h4>
                            <div className="space-y-2 text-sm">
                                <KeyInfoItem icon={<FaBalanceScale />} label="License" value={model.licensing} />
                                <div className="pt-2"><TransparencyInfo info={model.open_source_transparency} /></div>
                            </div>
                        </div>
                </div>
                {/* Right Column */}
                <div className="space-y-6">
                    <div>
                        <h4 className="font-semibold text-gray-800 mb-2">System Specs</h4>
                        <div className="space-y-2">
                            <KeyInfoItem icon={<FaMicrochip />} label="VRAM" value={model.specs.vram} />
                            <KeyInfoItem icon={<FaMemory />} label="System RAM" value={model.specs.ram} />
                            <KeyInfoItem icon={<FaHdd />} label="File Size" value={model.specs.file_size} />
                        </div>
                    </div>
                    <BenchmarkScores scores={model.benchmarks} />
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8">
                        
                        <div>
                            <InfoSection title="Quantization Availability" items={model.quantization} />
                        </div>
                    </div>
                    <InfoSection title="Ecosystem Compatibility" items={model.ecosystem_compatibility} />
                </div>
            </div>
        </div>
      </div>
      
      {/* --- TOGGLE BUTTON FOOTER --- */}
      <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
        <button 
            onClick={() => setIsExpanded(!isExpanded)} 
            className="w-full text-sm font-semibold text-blue-600 hover:text-blue-800 flex items-center justify-center"
        >
            {isExpanded ? 'View Less' : 'View More Details'}
            {isExpanded ? <FaChevronUp className="ml-2" /> : <FaChevronDown className="ml-2" />}
        </button>
      </div>
    </div>
  );
};
