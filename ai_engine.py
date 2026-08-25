"""
ai_engine.py — mBiz by Zorted Labs
====================================
Asynchronous AI Content Generation Pipeline     
- Universal AsyncOpenAI SDK connection    
- 10/10 Self-Reflective Audit Loop (up to 3 iterations)
- Multi-Angle Framework: Hook-Story, Lifestyle Flex, Value-Math
- NLP Front-Loading enforcement
- Banglish / localized dialect generation
"""

import os
import json
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mBiz_AI_Engine")

# ── SDK Client ──────────────────────────────────────────────────────────────
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.deepseek.com/v1")

if not AI_API_KEY:
    raise ValueError("❌ AI_API_KEY not found in .env — please set it before running.")

client = AsyncOpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)

# ── Language Options ────────────────────────────────────────────────────────

LANGUAGE_OPTIONS = {
    "🌐 Banglish (Bengali + English Mix)": {
        "code": "banglish",
        "instruction": "Write in **Trendy Banglish** (Bengali-English blend) — natural, conversational mix like how Dhaka/Gulshan/Rajshahi audiences actually speak. Use Bengali phrases naturally mixed with English. This is the default localized tone.",
    },
    "🇧🇩 Bangla (Full Bengali)": {
        "code": "bangla",
        "instruction": "Write entirely in **Bengali (Bangla)** — full Bengali language throughout. Use proper Bengali script for all content. No English words except for the product name and brand name if they are in English. Make it sound natural and native.",
    },
    "🇬🇧 English Only": {
        "code": "english",
        "instruction": "Write entirely in **English** — professional, persuasive English copy. No Bengali or Banglish mixing. Use a warm, conversational English tone suitable for a Bangladeshi audience but entirely in English.",
    },
}


# ── System Prompt Builder ───────────────────────────────────────────────────

def _build_system_prompt(language_code: str = "banglish") -> str:
    """Build the system prompt with the selected language instruction."""
    # Find the language instruction
    lang_instruction = LANGUAGE_OPTIONS["🌐 Banglish (Bengali + English Mix)"]["instruction"]
    for key, val in LANGUAGE_OPTIONS.items():
        if val["code"] == language_code:
            lang_instruction = val["instruction"]
            break

    return f"""You are **mBiz AI**, a world-class E-commerce/F-Commerce copywriter trained on 2026 Meta algorithm signals.

## Core Rules — NEVER BREAK THESE:

### 1. LANGUAGE — CRITICAL
{lang_instruction}

### 2. NLP Front-Loading (MANDATORY)
The FIRST 125 characters of Variation A's primary text MUST contain:
- [Product Name]
- [Core USP]
- [Target Location / City]
- [Target Model / Audience]
Do NOT start with vague hype like "Best quality product 🔥" or "Looking for...".

### 3. High-Weight Engagement Triggers
- Replace "Shop Now" with SAVE hooks: "Save this sizing chart for later 📌"
- Use 3+ word COMMENT prompts: "Comment 'INFO' + your city for a direct inbox video 🎯"
- Include SHARE triggers: "Tag a friend who needs this upgrade 👇"
- Use EMOTIONAL MICRO-HOOKS in the first line.

### 4. Multi-Angle Framework — Generate ALL 3 variations:
**Variation A — The Hook-Story Matrix:**
Relatable localized problem → emotional transformation → product as the hero. Start with a pain point your target audience feels daily.

**Variation B — The Lifestyle Flex:**
Aesthetic, social-proof heavy, compliments-focused. Make the reader feel like owning this product upgrades their status. Use visual language.

**Variation C — The Value-Math Engine:**
Smart breakdown of price vs. long-term utility. Compare cost-per-use, durability, or hidden savings. Make the reader feel smart for buying.

### 5. Forbidden Words
DO NOT use: "Shop now", "Buy now", "Best quality", "Premium quality", "Limited time offer" (unless genuinely true). Instead use: "Grab yours", "Reserve your fit", "Level up your [X]", "Upgrade your [Y]".

### 6. Format
Return ONLY valid JSON with this exact structure — no markdown fences, no extra text:
{{
  "variation_a": {{
    "headline": "...",
    "body": "..."
  }},
  "variation_b": {{
    "headline": "...",
    "body": "..."
  }},
  "variation_c": {{
    "headline": "...",
    "body": "..."
  }}
}}
"""

# ── Evaluation Prompt ───────────────────────────────────────────────────────

EVALUATION_PROMPT = """You are an elite Meta Algorithm Auditor. Score the following Facebook post copy from 1-10 across these dimensions:

1. **NLP Front-Loading** (first 125 chars contain product name, USP, location, audience)
2. **Engagement Trigger Density** (save hooks, comment prompts, share triggers)
3. **Persuasion & Emotional Resonance** (does it make you feel / act?)
4. **2026 Algorithm Readiness** (avoids spam signals, uses high-CTR patterns)
5. **Localized Authenticity** (Banglish / dialect feels natural, not forced)

Return ONLY valid JSON:
{
  "scores": {
    "nlp_front_loading": 0-10,
    "engagement_triggers": 0-10,
    "persuasion": 0-10,
    "algorithm_readiness": 0-10,
    "localization": 0-10
  },
  "overall": 0-10,
  "passed": true/false,
  "issues": ["issue1", "issue2", ...],
  "fix_instructions": "Specific instructions on what to fix."
}
"""


# ── Generation Helpers ──────────────────────────────────────────────────────

def _build_user_prompt(
    product_name: str,
    product_category: str,
    core_usp: str,
    target_location: str,
    target_audience: str,
    additional_context: str = "",
    language_code: str = "banglish",
) -> str:
    """Build the user prompt from structured inputs."""
    # Get language display name
    lang_display = "Banglish (Bengali + English Mix)"
    for key, val in LANGUAGE_OPTIONS.items():
        if val["code"] == language_code:
            lang_display = key
            break

    return f"""Generate 3 high-conversion Facebook post variations for:

Product Name: {product_name}
Category: {product_category}
Core USP: {core_usp}
Target Location: {target_location}
Target Audience: {target_audience}
Additional Context: {additional_context}

Language Preference: {lang_display}

Remember:
- Write in the EXACT language specified above — do not mix languages unless Banglish is selected
- NLP Front-Loading in first 125 chars of Variation A
- Save hooks, comment prompts, share triggers
- NO "Shop Now" or "Best quality"
- 3 variations: Hook-Story, Lifestyle Flex, Value-Math"""


async def _call_llm(messages: list, temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
    """Generic async LLM call with error handling."""
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return None


async def _generate_content(user_prompt: str, language_code: str = "banglish") -> Optional[dict]:
    """Generate the 3 variations from the AI."""
    system_prompt = _build_system_prompt(language_code)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    raw = await _call_llm(messages, temperature=0.8)
    if not raw:
        return None

    # Strip markdown fences if the model wraps output
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    if raw.startswith("json"):
        raw = raw[4:].strip()

    try:
        parsed = json.loads(raw)
        # Validate structure
        for key in ("variation_a", "variation_b", "variation_c"):
            if key not in parsed:
                logger.warning(f"Missing key: {key}")
                return None
            if not isinstance(parsed[key], dict):
                return None
            if "headline" not in parsed[key] or "body" not in parsed[key]:
                return None
        return parsed
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {e}")
        logger.debug(f"Raw output: {raw[:500]}")
        return None


async def _evaluate_content(content: dict) -> Optional[dict]:
    """Run the self-evaluation audit on generated content."""
    content_str = json.dumps(content, indent=2)
    messages = [
        {"role": "system", "content": EVALUATION_PROMPT},
        {"role": "user", "content": f"Evaluate this content:\n\n{content_str}"},
    ]
    raw = await _call_llm(messages, temperature=0.3, max_tokens=1000)
    if not raw:
        return None

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    if raw.startswith("json"):
        raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error(f"Evaluation JSON parse failed: {e}")
        return None


async def _regenerate_with_fixes(user_prompt: str, fix_instructions: str, language_code: str = "banglish") -> Optional[dict]:
    """Regenerate content incorporating fix instructions from the audit."""
    system_prompt = _build_system_prompt(language_code)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
        {
            "role": "assistant",
            "content": "I will generate the content following all rules carefully.",
        },
        {
            "role": "user",
            "content": f"IMPORTANT FIXES NEEDED:\n{fix_instructions}\n\nPlease regenerate all 3 variations with these fixes applied. Return ONLY valid JSON.",
        },
    ]
    raw = await _call_llm(messages, temperature=0.6)
    if not raw:
        return None

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0]
    if raw.startswith("json"):
        raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


# ── Public API ──────────────────────────────────────────────────────────────

async def generate_facebook_content(
    product_name: str,
    product_category: str,
    core_usp: str,
    target_location: str,
    target_audience: str,
    additional_context: str = "",
    language_code: str = "banglish",
    max_iterations: int = 3,
) -> dict:
    """
    Full generation pipeline with self-reflective audit loop.

    Returns:
    {
        "success": True/False,
        "content": { variation_a: {...}, variation_b: {...}, variation_c: {...} },
        "audit_log": [
            { "iteration": 1, "overall": 7, "passed": False, "issues": [...], "fix": "..." },
            ...
        ],
        "final_score": 10,
        "error": None or "error message"
    }
    """
    result = {
        "success": False,
        "content": None,
        "audit_log": [],
        "final_score": 0,
        "error": None,
    }

    user_prompt = _build_user_prompt(
        product_name, product_category, core_usp,
        target_location, target_audience, additional_context,
        language_code,
    )

    # ── Iteration 1: Initial Generation ──
    logger.info(f"🚀 Generating initial content (language: {language_code})...")
    content = await _generate_content(user_prompt, language_code)
    if not content:
        result["error"] = "Failed to generate initial content. Check API key and try again."
        return result

    # ── Self-Reflective Audit Loop ──
    for iteration in range(1, max_iterations + 1):
        logger.info(f"🔍 Audit iteration {iteration}/{max_iterations}...")
        evaluation = await _evaluate_content(content)

        if not evaluation:
            logger.warning(f"Evaluation failed on iteration {iteration}, accepting current content.")
            result["content"] = content
            result["final_score"] = 0
            result["success"] = True
            return result

        overall = evaluation.get("overall", 0)
        passed = evaluation.get("passed", False)
        issues = evaluation.get("issues", [])
        fix_instructions = evaluation.get("fix_instructions", "")

        result["audit_log"].append({
            "iteration": iteration,
            "overall": overall,
            "passed": passed,
            "issues": issues,
            "fix": fix_instructions,
        })

        logger.info(f"Iteration {iteration}: Score {overall}/10 — {'✅ PASSED' if passed else '❌ FAILED'}")

        if passed and overall >= 10:
            result["content"] = content
            result["final_score"] = overall
            result["success"] = True
            logger.info("🎯 10/10 achieved! Content is audit-approved.")
            return result

        if iteration < max_iterations and fix_instructions:
            logger.info(f"🔄 Regenerating with fixes (iteration {iteration + 1})...")
            content = await _regenerate_with_fixes(user_prompt, fix_instructions, language_code)
            if not content:
                logger.warning("Regeneration failed, using previous content.")
                break
        else:
            break

    # ── Fallback: Accept best attempt ──
    result["content"] = content
    result["final_score"] = result["audit_log"][-1]["overall"] if result["audit_log"] else 0
    result["success"] = True
    logger.info(f"📊 Best score: {result['final_score']}/10 — delivering content.")
    return result


# ── CLI Test Harness ────────────────────────────────────────────────────────

if __name__ == "__main__":
    async def test():
        result = await generate_facebook_content(
            product_name="LuxeFit Slim Blazer",
            product_category="Men's Fashion",
            core_usp="Stretch fabric, wrinkle-free, tailored fit for Bangladeshi men",
            target_location="Dhaka, Bangladesh",
            target_audience="Professional men aged 25-45 in Gulshan, Banani, Uttara",
            additional_context="Office wear + casual dinner vibe. Price: ৳3,500",
            language_code="banglish",
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    asyncio.run(test())
