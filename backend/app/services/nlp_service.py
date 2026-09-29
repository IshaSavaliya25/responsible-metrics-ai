import re
from typing import Dict, List, Any


class NLPService:

    """
    NLP Service for research paper analysis.

    Detects:

    - Keywords
    - Research Problems
    - Methodology
    - Research Contributions
    - Key Findings
    """


    def __init__(self):

        # ======================================
        # RESEARCH PROBLEM INDICATORS
        # ======================================

        self.problem_indicators = [

            "problem",
            "challenge",
            "limitation",
            "limitations",
            "lack of",
            "gap",
            "issue",
            "difficulty",
            "however",
            "despite",
            "unclear",
            "insufficient",
            "inadequate",
            "need for"
        ]


        # ======================================
        # METHODOLOGY INDICATORS
        # ======================================

        self.methodology_indicators = [

            "methodology",
            "method",
            "methods",
            "approach",
            "framework",
            "model",
            "analysis was conducted",
            "we analyzed",
            "we analyse",
            "we propose",
            "this study uses",
            "this study used",
            "data were collected",
            "data was collected",
            "dataset",
            "sample",
            "experiment",
            "case study",
            "literature review",
            "systematic review",
            "bibliometric analysis",
            "qualitative analysis",
            "quantitative analysis"
        ]


        # ======================================
        # CONTRIBUTION INDICATORS
        # ======================================

        self.contribution_indicators = [

            "we propose",
            "this paper proposes",
            "this study proposes",
            "we introduce",
            "this paper introduces",
            "we present",
            "this paper presents",
            "our contribution",
            "contribution of this study",
            "we develop",
            "this research develops",
            "we provide",
            "this paper provides"
        ]


        # ======================================
        # FINDING INDICATORS
        # ======================================

        self.finding_indicators = [

            "results show",
            "results indicate",
            "findings show",
            "findings indicate",
            "we found",
            "we find",
            "this study shows",
            "this study demonstrates",
            "our results",
            "the analysis shows",
            "the results suggest",
            "we conclude",
            "conclusion",
            "reveals",
            "demonstrates"
        ]


    # ==========================================
    # CLEAN TEXT
    # ==========================================

    def clean_text(self, text: str) -> str:

        if not text:

            return ""


        # Remove excessive spaces

        text = re.sub(
            r"\s+",
            " ",
            text
        )


        # Remove repeated punctuation

        text = re.sub(
            r"\.{3,}",
            ".",
            text
        )


        return text.strip()


    # ==========================================
    # SPLIT INTO SENTENCES
    # ==========================================

    def split_sentences(
        self,
        text: str
    ) -> List[str]:

        if not text:

            return []


        text = self.clean_text(text)


        sentences = re.split(

            r'(?<=[.!?])\s+',

            text

        )


        clean_sentences = []


        for sentence in sentences:

            sentence = sentence.strip()


            word_count = len(
                sentence.split()
            )


            # Ignore very short or very long sentences

            if word_count >= 6 and word_count <= 100:

                clean_sentences.append(
                    sentence
                )


        return clean_sentences


    # ==========================================
    # REMOVE DUPLICATES
    # ==========================================

    def remove_duplicates(
        self,
        items: List[str]
    ) -> List[str]:

        unique_items = []

        seen = set()


        for item in items:

            normalized = item.lower().strip()


            if normalized not in seen:

                seen.add(
                    normalized
                )

                unique_items.append(
                    item
                )


        return unique_items


    # ==========================================
    # FIND SENTENCES USING INDICATORS
    # ==========================================

    def find_matching_sentences(

        self,

        sentences: List[str],

        indicators: List[str],

        limit: int = 5

    ) -> List[str]:


        matches = []


        for sentence in sentences:

            sentence_lower = sentence.lower()


            for indicator in indicators:

                if indicator in sentence_lower:

                    matches.append(
                        sentence
                    )

                    break


            if len(matches) >= limit:

                break


        return self.remove_duplicates(
            matches
        )


    # ==========================================
    # EXTRACT KEYWORDS
    # ==========================================

    def extract_keywords(

        self,

        text: str,

        max_keywords: int = 10

    ) -> List[Dict[str, Any]]:


        if not text:

            return []


        text = self.clean_text(
            text.lower()
        )


        # Attempt KeyBERT keyphrase extraction
        try:
            from keybert import KeyBERT
            from app.ml.embeddings import EmbeddingService
            emb_service = EmbeddingService()
            if not emb_service._use_fallback and emb_service._model is not None:
                kw_model = KeyBERT(model=emb_service._model)
                keyphrases = kw_model.extract_keywords(
                    text,
                    keyphrase_ngram_range=(1, 3),
                    stop_words="english",
                    top_n=max_keywords
                )
                if keyphrases:
                    return [
                        {"keyword": kp[0], "score": round(float(kp[1]), 4)}
                        for kp in keyphrases
                    ]
        except Exception as e:
            pass

        # Fallback to enhanced multi-gram frequency extraction
        stop_words = {
            "the", "and", "for", "with", "that", "this", "from", "are", "was",
            "were", "have", "has", "had", "into", "their", "there", "which",
            "about", "these", "those", "using", "used", "use", "study", "research",
            "paper", "article", "based", "also", "such", "than", "between",
            "within", "through", "more", "other", "can", "may", "will", "all"
        }

        # Extract unigrams and bigrams
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text)
        filtered_words = [w for w in words if w not in stop_words]

        frequency = {}
        for w in filtered_words:
            frequency[w] = frequency.get(w, 0) + 1

        # Bigrams
        for i in range(len(filtered_words) - 1):
            w1, w2 = filtered_words[i], filtered_words[i+1]
            if w1 != w2:
                bigram = f"{w1} {w2}"
                frequency[bigram] = frequency.get(bigram, 0) + 2

        sorted_phrases = sorted(
            frequency.items(),
            key=lambda item: item[1],
            reverse=True
        )

        keywords = []
        max_frequency = sorted_phrases[0][1] if sorted_phrases else 1

        for phrase, count in sorted_phrases[:max_keywords]:
            score = round(count / max_frequency, 4)
            keywords.append({
                "keyword": phrase,
                "score": score
            })

        return keywords


    # ==========================================
    # EXTRACT SECTION TEXT
    # ==========================================

    def get_section_text(

        self,

        sections: Dict[str, str],

        section_names: List[str]

    ) -> str:


        collected_text = []


        for section_name in section_names:

            section_text = sections.get(

                section_name,

                ""
            )


            if section_text:

                collected_text.append(
                    section_text
                )


        return " ".join(
            collected_text
        )


    # ==========================================
    # MAIN PAPER ANALYSIS
    # ==========================================

    def extract_key_phrases(

            self,

            text: str,

            max_phrases: int = 10

        ):

            if not text:

                return []


            text = self.clean_text(
                text.lower()
            )


            # Academic phrase patterns

            patterns = [

                r"\b(?:responsible|appropriate|effective|scientific|research|bibliometric|quantitative|qualitative)\s+(?:research|evaluation|indicators|metrics|analysis|framework)\b",

                r"\b[a-z]+\s+[a-z]+\s+(?:indicators|evaluation|analysis|framework|metrics)\b"

            ]


            phrases = []


            for pattern in patterns:

                matches = re.findall(

                    pattern,

                    text

                )


                phrases.extend(
                    matches
                )


            # Remove duplicates

            phrases = self.remove_duplicates(
                phrases
            )


            return [

                {

                    "keyword": phrase,

                    "score": round(

                        1 - (index * 0.05),

                        4

                    )

                }

                for index, phrase

                in enumerate(

                    phrases[:max_phrases]

                )

            ]

    def analyze_paper(

        self,

        sections: Dict[str, str]

    ) -> Dict[str, Any]:


        sections = sections or {}


        # ======================================
        # GET INDIVIDUAL SECTIONS
        # ======================================

        abstract_text = sections.get(
            "abstract",
            ""
        )


        introduction_text = sections.get(
            "introduction",
            ""
        )


        methodology_text = sections.get(
            "methodology",
            ""
        )


        results_text = sections.get(
            "results",
            ""
        )


        discussion_text = sections.get(
            "discussion",
            ""
        )


        conclusion_text = sections.get(
            "conclusion",
            ""
        )


        literature_review_text = sections.get(
            "literature_review",
            ""
        )


        # ======================================
        # BUILD MAIN TEXT
        # EXCLUDE REFERENCES
        # ======================================

        full_text = " ".join(

            [

                value

                for key, value in sections.items()

                if key != "references"

                and isinstance(value, str)

            ]

        )


        full_text = self.clean_text(
            full_text
        )


        # ======================================
        # CREATE SENTENCE GROUPS
        # ======================================

        introduction_sentences = (

            self.split_sentences(
                introduction_text
            )

        )


        methodology_sentences = (

            self.split_sentences(
                methodology_text
            )

        )


        results_sentences = (

            self.split_sentences(
                results_text
            )

        )


        discussion_sentences = (

            self.split_sentences(
                discussion_text
            )

        )


        conclusion_sentences = (

            self.split_sentences(
                conclusion_text
            )

        )


        full_sentences = (

            self.split_sentences(
                full_text
            )

        )


        # ======================================
        # KEYWORD EXTRACTION
        # ABSTRACT + INTRODUCTION
        # ======================================

        keyword_source = " ".join(

            [

                abstract_text,

                introduction_text

            ]

        )


        if not keyword_source.strip():

            keyword_source = full_text


        phrase_keywords = (

            self.extract_key_phrases(

                keyword_source,

                max_phrases=10

            )

        )


        word_keywords = (

            self.extract_keywords(

                keyword_source,

                max_keywords=10

            )

        )


        if len(phrase_keywords) >= 3:

            keywords = phrase_keywords

        else:

            keywords = word_keywords


        # ======================================
        # RESEARCH PROBLEM
        # INTRODUCTION + LITERATURE REVIEW
        # ======================================

        problem_sentences = (

            introduction_sentences

            +

            self.split_sentences(
                literature_review_text
            )

        )


        if not problem_sentences:

            problem_sentences = full_sentences


        research_problem = (

            self.find_matching_sentences(

                problem_sentences,

                self.problem_indicators,

                limit=5

            )

        )


        # ======================================
        # METHODOLOGY
        # METHODOLOGY SECTION
        # ======================================

        if methodology_sentences:

            methodology = (

                self.find_matching_sentences(

                    methodology_sentences,

                    self.methodology_indicators,

                    limit=5

                )

            )


            # If no indicator sentence found,
            # use first methodology sentences

            if not methodology:

                methodology = methodology_sentences[:5]


        else:

            # Fallback to full paper

            methodology = (

                self.find_matching_sentences(

                    full_sentences,

                    self.methodology_indicators,

                    limit=5

                )

            )


        # ======================================
        # CONTRIBUTIONS
        # INTRODUCTION + CONCLUSION
        # ======================================

        contribution_sentences = (

            introduction_sentences

            +

            conclusion_sentences

        )


        if not contribution_sentences:

            contribution_sentences = full_sentences


        contributions = (

            self.find_matching_sentences(

                contribution_sentences,

                self.contribution_indicators,

                limit=5

            )

        )


        # ======================================
        # KEY FINDINGS
        # RESULTS + DISCUSSION + CONCLUSION
        # ======================================

        finding_sentences = (

            results_sentences

            +

            discussion_sentences

            +

            conclusion_sentences

        )


        if not finding_sentences:

            finding_sentences = full_sentences


        key_findings = (

            self.find_matching_sentences(

                finding_sentences,

                self.finding_indicators,

                limit=5

            )

        )


        # ======================================
        # FALLBACK FINDINGS
        # ======================================

        if not key_findings:

            key_findings = (

                conclusion_sentences[:3]

                if conclusion_sentences

                else []

            )


        # ======================================
        # RETURN STRUCTURED ANALYSIS
        # ======================================

        return {

            "keywords":

                keywords,


            "research_problem":

                research_problem,


            "methodology":

                methodology,


            "contributions":

                contributions,


            "key_findings":

                key_findings,


            "sections_used": {

                "keywords":

                    [

                        "abstract",

                        "introduction"

                    ],


                "research_problem":

                    [

                        "introduction",

                        "literature_review"

                    ],


                "methodology":

                    [

                        "methodology"

                    ],


                "contributions":

                    [

                        "introduction",

                        "conclusion"

                    ],


                "key_findings":

                    [

                        "results",

                        "discussion",

                        "conclusion"

                    ]

            },


            "statistics": {

                "total_sections":

                    len(sections),


                "total_sentences":

                    len(full_sentences),


                "total_characters":

                    len(full_text),


                "sections_detected":

                    list(sections.keys())

            }

        }