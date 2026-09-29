import httpx

from app.config import settings
from rapidfuzz import fuzz


class OpenAlexService:

    @staticmethod
    async def search_paper_by_title(title: str):
        """
        Search OpenAlex and find the best matching paper.
        """

        if not title or len(title.strip()) < 5:
            return None

        url = f"{settings.OPENALEX_BASE_URL}/works"

        params = {
            "search": title,
            "per-page": 10
        }

        if settings.OPENALEX_EMAIL:
            params["mailto"] = settings.OPENALEX_EMAIL

        try:

            async with httpx.AsyncClient(
                timeout=20.0
            ) as client:

                response = await client.get(
                    url,
                    params=params
                )

                response.raise_for_status()

                data = response.json()

                results = data.get(
                    "results",
                    []
                )

                if not results:
                    return None

                best_match = None
                highest_score = 0

                for work in results:

                    work_title = work.get(
                        "title",
                        ""
                    )

                    score = fuzz.token_sort_ratio(
                        title.lower(),
                        work_title.lower()
                    )

                    if score > highest_score:

                        highest_score = score

                        best_match = work

                # Minimum similarity threshold
                if highest_score < 60:
                    return None

                return best_match

        except httpx.HTTPError as e:

            raise Exception(
                f"OpenAlex API request failed: {str(e)}"
            )


    @staticmethod
    def extract_bibliometric_data(work: dict) -> dict:
        """
        Extract relevant bibliometric information
        from OpenAlex API response.
        """

        if not work:
            return {}

        authorships = work.get(
            "authorships",
            []
        )

        authors = []

        institutions = []

        for authorship in authorships:

            author = authorship.get(
                "author",
                {}
            )

            if author:

                authors.append(
                    author.get(
                        "display_name",
                        "Unknown"
                    )
                )

            for institution in authorship.get(
                "institutions",
                []
            ):

                institution_name = institution.get(
                    "display_name"
                )

                if institution_name:

                    institutions.append(
                        institution_name
                    )

        primary_location = work.get(
            "primary_location",
            {}
        )

        source = primary_location.get(
            "source",
            {}
        ) or {}

        return {

            "openalex_id": work.get("id"),

            "doi": work.get("doi"),

            "title": work.get("title"),

            "publication_year": work.get(
                "publication_year"
            ),

            "publication_date": work.get(
                "publication_date"
            ),

            "citation_count": work.get(
                "cited_by_count",
                0
            ),

            "author_count": len(authors),

            "authors": authors,

            "institutions": list(
                set(institutions)
            ),

            "journal": source.get(
                "display_name"
            ),

            "journal_type": source.get(
                "type"
            ),

            "reference_count": work.get(
                "referenced_works_count",
                0
            ),

            "open_access": work.get(
                "open_access",
                {}
            ),

            "language": work.get(
                "language"
            ),

            "type": work.get(
                "type"
            )
        }