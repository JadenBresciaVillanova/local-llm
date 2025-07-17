// frontend/src/lib/model-data.ts

// 1. Define the updated structure of our model information
export interface ModelInfo {
  // Core Identity
  id: string;
  name: string;
  architecture: string;
  param_count: string;
  
  // Functional Characteristics
  type: string;
  intended_use: string;
  summary: string;
  dialogue_style: string;
  context_length: string;
  knowledge_cutoff: string;
  domain_specialization: 'General' | 'Code' | 'Multi-modal' | 'Research';

  // Performance & Specs
  latency?: string;
  specs: {
    vram: string;
    ram: string;
    file_size: string;
  };
  quantization: string[];
  
  // Strengths & Weaknesses
  advantages: string[];
  weaknesses: string[];
  
  // Ecosystem & Community
  use_cases: string[];
  ecosystem_compatibility: string[];
  licensing: string;
  open_source_transparency: {
    has_weights: boolean;
    has_details: boolean;
    link?: string;
  };
  
  // Standardized Benchmarks
  benchmarks?: {
    mt_bench?: number;
    mmlu?: number;
    gsm8k?: number;
    human_eval?: number;
  };
}


// 2. Create the array of model data with the new, richer format.
export const MODEL_DATA: ModelInfo[] = [
  {
    // Core Identity
    id: "llama3:8b",
    name: "llama3:8b",
    architecture: "Llama 3",
    param_count: "8 Billion",
    
    // Functional Characteristics
    type: "Instruction-Tuned",
    intended_use: "General Chat & Assistant Tasks",
    summary: "A highly capable, general-purpose small language model (SLM) developed by Meta. It excels at following instructions, reasoning, and provides a great balance of performance and resource requirements. It's the recommended default for most chat-based applications.",
    dialogue_style: "Helpful, direct, and factual, but can adopt creative tones when prompted.",
    context_length: "8,192 tokens",
    knowledge_cutoff: "March 2023",
    domain_specialization: 'General',

    // Performance & Specs
    specs: {
      vram: "~6.7 GB",
      ram: "8 GB+",
      file_size: "4.7 GB"
    },
    quantization: ["Q4_0", "Q4_K_M", "Q5_K_M", "Q8_0"],
    
    // Strengths & Weaknesses
    advantages: [
      "Excellent instruction following for its size.",
      "Strong reasoning and language capabilities.",
      "Fast inference speed on consumer hardware.",
      "Relatively low VRAM and RAM requirements."
    ],
    weaknesses: [
      "Not specialized for coding tasks (though still competent).",
      "Not multi-modal (cannot process images or audio).",
      "Can occasionally hallucinate facts if not grounded by RAG."
    ],
    
    // Ecosystem & Community
    use_cases: [
      "General purpose chatbot / AI assistant.",
      "Summarization and content creation.",
      "Retrieval-Augmented Generation (RAG) with documents.",
      "Simple classification and data extraction tasks."
    ],
    ecosystem_compatibility: ["Ollama", "Hugging Face Transformers", "LangChain", "Llama.cpp"],
    licensing: "Llama 3 License (Permissive, allows commercial use with conditions)",
    open_source_transparency: {
      has_weights: true,
      has_details: true,
      link: "https://llama.meta.com/llama3/"
    },

    // Standardized Benchmarks
    benchmarks: {
      mt_bench: 8.97,
      mmlu: 66.6,
      gsm8k: 82.8,
      human_eval: 62.2,
    }
  },
  {
    // Core Identity
    id: "codellama",
    name: "codellama",
    architecture: "Llama 2",
    param_count: "7 Billion",
    
    // Functional Characteristics
    type: "Code Generation",
    intended_use: "Code completion, generation, and explanation.",
    summary: "A version of Llama 2 specifically fine-tuned on a massive dataset of code. It supports a wide variety of popular programming languages and is the go-to model for any programming-related tasks.",
    dialogue_style: "Technical and code-focused, provides explanations in comments or markdown.",
    context_length: "16,384 tokens (can support up to 100k)",
    knowledge_cutoff: "July 2023",
    domain_specialization: 'Code',

    // Performance & Specs
    specs: {
      vram: "~6 GB",
      ram: "8 GB+",
      file_size: "3.8 GB"
    },
    quantization: ["Q4_0", "Q4_K_M", "Q5_K_M", "Q8_0"],
    
    // Strengths & Weaknesses
    advantages: [
      "Top-tier performance on coding benchmarks.",
      "Supports code in-filling and instruction following for code.",
      "Large context window is ideal for repository-level questions.",
      "Available in multiple parameter sizes (7B, 13B, 34B)."
    ],
    weaknesses: [
      "General chat and reasoning capabilities are weaker than instruction-tuned models.",
      "Not suitable for creative writing or non-technical tasks."
    ],
    
    // Ecosystem & Community
    use_cases: [
      "Writing new functions or classes from a docstring.",
      "Explaining complex code blocks in plain English.",
      "Translating code from one language to another (e.g., Python to JavaScript).",
      "Debugging and code completion."
    ],
    ecosystem_compatibility: ["Ollama", "Hugging Face Transformers", "LangChain", "VS Code"],
    licensing: "Llama 2 License (Permissive, allows commercial use)",
    open_source_transparency: {
      has_weights: true,
      has_details: true,
      link: "https://ai.meta.com/blog/code-llama-large-language-model-coding/"
    },

    // Standardized Benchmarks
    benchmarks: {
        human_eval: 53, // Score for the base 7B model
        gsm8k: 46.8,
    }
  },
  {
    // Core Identity
    id: "mistral",
    name: "mistral",
    architecture: "Mistral",
    param_count: "7 Billion",
    
    // Functional Characteristics
    type: "Instruction-Tuned",
    intended_use: "High-performance general chat.",
    summary: "A powerful model from Mistral AI, famous for its performance that rivals much larger models. It uses advanced techniques like Sliding Window Attention (SWA) and Grouped-Query Attention (GQA) for extreme efficiency.",
    dialogue_style: "Concise, direct, and performs well on a wide range of tasks.",
    context_length: "8,192 tokens (effective window of 32k via SWA)",
    knowledge_cutoff: "July 2023",
    domain_specialization: 'General',

    // Performance & Specs
    specs: {
      vram: "~6 GB",
      ram: "8 GB+",
      file_size: "4.1 GB"
    },
    quantization: ["Q4_0", "Q5_K_M", "Q8_0"],
    
    // Strengths & Weaknesses
    advantages: [
      "Extremely strong performance for its size, often outperforming 13B+ models.",
      "Very fast and memory-efficient due to attention mechanisms.",
      "Apache 2.0 license is highly permissive for any use case.",
      "Great at both English and Code tasks."
    ],
    weaknesses: [
      "Base model has fewer safety guardrails than commercially hosted versions.",
      "Can be less creative than some other models."
    ],
    
    // Ecosystem & Community
    use_cases: [
      "Efficient, low-latency chatbot applications.",
      "Summarization and document Q&A.",
      "As a general-purpose tool for developers."
    ],
    ecosystem_compatibility: ["Ollama", "Hugging Face Transformers", "LangChain", "vLLM"],
    licensing: "Apache 2.0 (Fully Permissive)",
    open_source_transparency: {
      has_weights: true,
      has_details: true,
      link: "https://mistral.ai/news/announcing-mistral-7b/"
    },

    // Standardized Benchmarks
    benchmarks: {
      mt_bench: 8.3,
      mmlu: 62.5,
      gsm8k: 58.4,
      human_eval: 40.2,
    }
  },
  {
    // Core Identity
    id: "dolphin-mistral:7b",
    name: "dolphin-mistral",
    architecture: "Mistral (Fine-tune)",
    param_count: "7 Billion",
    
    // Functional Characteristics
    type: "Uncensored, Instruction-Tuned",
    intended_use: "Coding and general tasks with less filtering.",
    summary: "A popular fine-tuned version of Mistral by Eric Hartford, optimized for coding and providing less-guarded, more direct responses. It's a favorite among developers for its utility and unfiltered nature.",
    dialogue_style: "Helpful and direct, often used for brainstorming and coding.",
    context_length: "8,192 tokens",
    knowledge_cutoff: "July 2023",
    domain_specialization: 'Code',

    // Performance & Specs
    specs: {
      vram: "~6 GB",
      ram: "8 GB+",
      file_size: "4.1 GB"
    },
    quantization: ["Q4_0", "Q5_K_M", "Q8_0"],
    
    // Strengths & Weaknesses
    advantages: [
      "Excellent coding and reasoning abilities, often surpassing the base model.",
      "Less 'refusal' to answer prompts compared to heavily filtered models.",
      "Great for creative and development-focused use cases."
    ],
    weaknesses: [
      "Lack of safety guardrails means it can produce undesirable or unsafe content.",
      "Not suitable for public-facing applications without an additional safety layer.",
    ],
    
    // Ecosystem & Community
    use_cases: [
      "Developer assistant for coding and debugging.",
      "Unfiltered brainstorming and content generation.",
      "Role-playing and creative story writing."
    ],
    ecosystem_compatibility: ["Ollama", "Hugging Face Transformers", "GGUF"],
    licensing: "Apache 2.0 (based on Mistral)",
    open_source_transparency: {
      has_weights: true,
      has_details: false, // Fine-tuning details are on the Hugging Face card
      link: "https://huggingface.co/ehartford/dolphin-2.2.1-mistral-7b"
    },
  },
  {
    // Core Identity
    id: "llava",
    name: "llava",
    architecture: "LLaVA (based on Vicuna)",
    param_count: "7 Billion",
    
    // Functional Characteristics
    type: "Multi-modal (Text & Vision)",
    intended_use: "Describing images and answering questions about them.",
    summary: "A large multi-modal model (LMM) that can understand both text and images. You can provide an image and ask questions about it, combining vision and language understanding.",
    dialogue_style: "Descriptive and conversational, focused on the content of the image.",
    context_length: "2,048 tokens",
    knowledge_cutoff: "N/A (Vision Model)",
    domain_specialization: 'Multi-modal',

    // Performance & Specs
    specs: {
      vram: "~8 GB",
      ram: "16 GB+",
      file_size: "4.5 GB + Vision Model"
    },
    quantization: ["Q4_K_M", "Q5_K_M"],
    
    // Strengths & Weaknesses
    advantages: [
      "Ability to 'see' and interpret visual information.",
      "Enables new use cases not possible with text-only models.",
      "Good at general object recognition and scene description."
    ],
    weaknesses: [
      "Text-only reasoning is weaker than dedicated text models of the same size.",
      "Can be prone to 'hallucinating' details in images that are not there.",
      "Requires more VRAM due to the separate vision encoder.",
      "UI for image uploads is more complex."
    ],
    
    // Ecosystem & Community
    use_cases: [
      "Making websites accessible by describing images for screen readers.",
      "Analyzing charts and graphs to extract data.",
      "Answering visual questions like 'What color is the car in this picture?'."
    ],
    ecosystem_compatibility: ["Ollama", "LLaVA-Next project"],
    licensing: "Llama 2 License (based on Vicuna)",
    open_source_transparency: {
      has_weights: true,
      has_details: true,
      link: "https://llava-vl.github.io/"
    },
  },
  {
    // Core Identity
    id: "gemma:7b",
    name: "gemma:7b",
    architecture: "Gemma",
    param_count: "7 Billion",
    
    // Functional Characteristics
    type: "Instruction-Tuned",
    intended_use: "High-performance general chat, from Google.",
    summary: "A family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models. It offers a great balance of performance and responsible design.",
    dialogue_style: "Helpful and safe, with a strong focus on responsible AI principles.",
    context_length: "8,192 tokens",
    knowledge_cutoff: "October 2023",
    domain_specialization: 'General',

    // Performance & Specs
    specs: {
      vram: "~6.5 GB",
      ram: "8 GB+",
      file_size: "4.8 GB"
    },
    quantization: ["Q4_0", "Q5_K_M", "Q8_0"],
    
    // Strengths & Weaknesses
    advantages: [
      "Strong all-around performance on a variety of benchmarks.",
      "Backed by Google's research and infrastructure.",
      "Designed with a focus on safety and responsibility.",
      "Highly permissive license for commercial use."
    ],
    weaknesses: [
      "Newer than other models, so the fine-tuning ecosystem is still growing.",
      "Can be more cautious or refuse to answer some prompts due to safety tuning."
    ],
    
    // Ecosystem & Community
    use_cases: [
      "General chatbot and assistant roles.",
      "Content generation for blogs and marketing.",
      "Safe, public-facing applications."
    ],
    ecosystem_compatibility: ["Ollama", "Hugging Face Transformers", "LangChain", "Keras"],
    licensing: "Gemma Terms of Use (Permissive, allows commercial use)",
    open_source_transparency: {
      has_weights: true,
      has_details: true,
      link: "https://blog.google/technology/developers/gemma-open-models/"
    },

    // Standardized Benchmarks
    benchmarks: {
      mt_bench: 7.9,
      mmlu: 64.3,
      gsm8k: 74.3,
      human_eval: 32.3,
    }
  },
];