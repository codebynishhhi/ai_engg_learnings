import re


def split_into_paragraphs(text: str) -> list[str]:
    paragraphs = text.split("\n\n")

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_large_paragraph(
    paragraph: str,
    max_characters: int
) -> list[str]:

    sentences = split_into_sentences(paragraph)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        # Case 1: Sentence itself is too large
        if len(sentence) > max_characters:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            sentence_chunks = []

            for start in range(
                0,
                len(sentence),
                max_characters
            ):
                sentence_chunks.append(
                    sentence[start:start + max_characters]
                )

            chunks.extend(sentence_chunks)

        # Case 2: Sentence fits into current chunk
        elif len(current_chunk) + len(sentence) + 1 <= max_characters:

            if current_chunk:
                current_chunk += " "

            current_chunk += sentence

        # Case 3: Sentence doesn't fit into current chunk
        else:

            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def get_overlap_sentences(
    sentences: list[str],
    overlap_characters: int
) -> list[str]:

    overlap_sentences = []
    current_length = 0

    for sentence in reversed(sentences):

        sentence_length = len(sentence)

        if (
            current_length + sentence_length
            <= overlap_characters
        ):
            overlap_sentences.insert(0, sentence)
            current_length += sentence_length

        else:
            break

    return overlap_sentences


def create_chunks(
    paragraphs: list[str],
    max_characters: int = 100,
    overlap_characters: int = 20
) -> list[str]:

    chunks = []
    current_sentences = []

    for paragraph in paragraphs:

        sentences = split_into_sentences(paragraph)

        for sentence in sentences:

            # Sentence itself is too large
            if len(sentence) > max_characters:

                if current_sentences:
                    chunks.append(
                        " ".join(current_sentences)
                    )
                    current_sentences = []

                large_chunks = split_large_paragraph(
                    sentence,
                    max_characters
                )

                chunks.extend(large_chunks)
                continue

            current_length = sum(
                len(item)
                for item in current_sentences
            )

            separator_length = (
                len(current_sentences) - 1
                if current_sentences
                else 0
            )

            proposed_length = (
                current_length
                + separator_length
                + len(sentence)
                + (1 if current_sentences else 0)
            )

            # Sentence fits
            if proposed_length <= max_characters:

                current_sentences.append(sentence)

            # Sentence doesn't fit
            else:

                if current_sentences:
                    chunks.append(
                        " ".join(current_sentences)
                    )

                # Create overlap for next chunk
                current_sentences = get_overlap_sentences(
                    current_sentences,
                    overlap_characters
                )

                current_sentences.append(sentence)

    # Save final chunk
    if current_sentences:
        chunks.append(
            " ".join(current_sentences)
        )

    return chunks


if __name__ == "__main__":

    # paragraph = (
    #     "Artificial intelligence is transforming software engineering. "
    #     "Large language models can assist developers with coding and documentation. "
    #     "Production AI systems require evaluation, monitoring, and security controls."
    # )

    # print("===== SENTENCES =====")

    # sentences = split_into_sentences(paragraph)

    # for index, sentence in enumerate(sentences, start=1):
    #     print(f"\nSentence {index}")
    #     print(sentence)
    #     print(f"Characters: {len(sentence)}")

    # print("\n===== OVERLAP SENTENCES =====")

    # overlap_sentences = get_overlap_sentences(
    #     sentences,
    #     overlap_characters=80
    # )

    # for index, sentence in enumerate(
    #     overlap_sentences,
    #     start=1
    # ):
    #     print(f"\nOverlap Sentence {index}")
    #     print(sentence)

    # print("\n===== LARGE PARAGRAPH CHUNKS =====")

    # chunks = split_large_paragraph(
    #     paragraph,
    #     max_characters=100
    # )

    # for index, chunk in enumerate(chunks, start=1):
    #     print(f"\nChunk {index}")
    #     print(chunk)
    #     print(f"Characters: {len(chunk)}")
    paragraphs = [
    (
        "Artificial intelligence is transforming software engineering. "
        "Large language models can assist developers with coding and documentation. "
        "Production AI systems require evaluation, monitoring, and security controls. "
        "Reliable evaluation is important for production AI systems."
    )
]

    chunks = create_chunks(
        paragraphs,
        max_characters=150,
        overlap_characters=100
    )

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n===== Chunk {index} =====")
        print(chunk)
        print(f"Characters: {len(chunk)}")