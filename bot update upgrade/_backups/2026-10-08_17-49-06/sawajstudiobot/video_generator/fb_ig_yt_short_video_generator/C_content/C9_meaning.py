# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C9_meaning.py                             ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                C_content/C9_meaning.py                   ║
# ║  🎯 PURPOSE:   ⭐ Hindi Meaning Generator (NEW!)         ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📖 HINDI MEANING MODULE                                ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Hadith ka Hindi matlab (explanation) generate karna ║
║                                                          ║
║   📖 What it does:                                       ║
║      1. Hadith text (Hindi translation) leta hai         ║
║      2. AI se meaning (2-3 lines) banata hai             ║
║      3. Simple Hindi mein — aam aadmi ke liye            ║
║                                                          ║
║   📊 Output:                                              ║
║      Simple Hindi meaning text (2-3 lines)               ║
║                                                          ║
║   📖 Example:                                             ║
║      Input: "अमल का दारोमदार नीयतों पर है।"               ║
║      Output: "इस हदीस में नीयत की अहमियत बताई गई है।       ║
║               हर अमल का दारोमदार नीयत पर है। अगर          ║
║               नीयत साफ है, तो छोटा अमल भी बड़ा            ║
║               बन जाता है।"                                ║
║                                                          ║
║   ⚠️  Sirf Short + Long mein use hoga:                    ║
║      Story: 50-60s — koi meaning nahi                     ║
║      Short: 1-3 min — meaning included                    ║
║      Long:  5-15 min — meaning + commentary               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


class Meaning:
    """
    Generate Hindi meaning of hadith using AI.

    Simple Hindi mein — aam aadmi ke liye.
    """

    def __init__(self, base, ai):
        log_file_start("C9_meaning.py", "Hindi meaning generator")
        self.base = base
        self.ai = ai
        log_file_end("C9_meaning.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    # ① GENERATE — Hindi matlab banao
    # ─────────────────────────────────────────────────────
    def generate(self, hadith_hindi):
        """
        Generate Hindi meaning from hadith.

        Args:
            hadith_hindi: Hadith text in Hindi

        Returns:
            Meaning text (2-3 lines in Hindi)
        """
        log_step("C9_meaning.py", "generate() starting", "ok",
                 f"hadith {len(hadith_hindi)} chars")

        if not hadith_hindi:
            log_step("C9_meaning.py", "Empty hadith", "fail")
            return self._fallback()

        # ═══════════ Prompt for AI ═══════════
        prompt = (
            f"Is Hadith ka short aur simple Hindi matlab likho.\n\n"
            f"Rules:\n"
            f"- Sirf Hindi mein\n"
            f"- 2-3 lines max\n"
            f"- Simple words (aam aadmi samajh sake)\n"
            f"- Soft aur dil ko chhune wala\n"
            f"- Sirf matlab — koi extra baat nahi\n"
            f"- Hadith ki sikh (lesson) highlight karo\n\n"
            f"Hadith:\n{hadith_hindi}\n\n"
            f"Ab Hindi matlab likho:"
        )

        # ═══════════ Call AI ═══════════
        result = self.ai.call(prompt, max_tokens=300, task="meaning")

        if result:
            # ═══════════ Clean result ═══════════
            meaning = sanitize(result)
            # Remove markdown code blocks if any
            meaning = meaning.replace("```", "").strip()
            # Remove common prefixes
            for prefix in ["Hindi matlab:", "Matlab:", "Meaning:", "हिंदी मतलब:"]:
                if meaning.startswith(prefix):
                    meaning = meaning[len(prefix):].strip()

            if len(meaning) > 20:
                log_step("C9_meaning.py", "Meaning generated", "ok",
                         f"{len(meaning)} chars")
                self.base.api_status["AI"]["meaning"] = "success"
                return meaning

        # ═══════════ Fallback ═══════════
        log_step("C9_meaning.py", "AI failed, using fallback", "warn")
        return self._fallback()

    # ─────────────────────────────────────────────────────
    # ② FALLBACK — default meaning
    # ─────────────────────────────────────────────────────
    def _fallback(self):
        """Return default meaning if AI fails."""
        return (
            "इस हदीस में नीयत की अहमियत बताई गई है। "
            "हर अमल का दारोमदार नीयत पर है। "
            "अगर नीयत साफ है, तो छोटा अमल भी बड़ा बन जाता है।"
        )
