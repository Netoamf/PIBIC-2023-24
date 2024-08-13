def compare_morphemes_to_file(lexicon, morphemes_filename, output_filename):
    """
    Compares morphemes and writes the best matches to a file.
    :param lexicon: Lexicon to compare against.
    :param morphemes_filename: File containing morphemes.
    :param output_filename: File to write the comparison results.
    :return: Number of best matches found and total morphemes.
    """
    best_matches_found = 0
    total_morphemes = 0

    with open(morphemes_filename, "r", encoding="utf-8") as morphemes_file, open(output_filename, "w", encoding="utf-8") as output_file:
        for morpheme in morphemes_file:
            morpheme = morpheme.strip()
            morpheme_set = set(morpheme.split())  # converte os morfemas em um set
            best_match = None
            best_match_size = 0
            for segment in lexicon.keys():
                segment_set = set(segment.split())  # converte segmentos em um set
                intersection = morpheme_set & segment_set  # Interseção
                union = morpheme_set | segment_set  # União
                if len(intersection) > best_match_size:
                    best_match = segment
                    best_match_size = len(intersection)
            if best_match is not None:
                output_file.write(f"Linha alvo: '{morpheme}' - Melhor correspondência: '{best_match}' (com {best_match_size} palavras em comum)\n")
                best_matches_found += 1
            else:
                output_file.write(f"Linha alvo: '{morpheme}' - Nenhuma correspondência encontrada\n")
            total_morphemes += 1

    return best_matches_found, total_morphemes

def compare_segmentations_to_file(lexicon, morphemes_filename, output_filename):
    """
    Compares segmentations and writes the best matches to a file.
    :param lexicon: Lexicon to compare against.
    :param morphemes_filename: File containing morphemes.
    :param output_filename: File to write the comparison results.
    :return: Number of best matches found and total morphemes.
    """
    best_matches_found = 0
    total_morphemes = 0

    with open(morphemes_filename, "r", encoding="utf-8") as morphemes_file, open(output_filename, "w", encoding="utf-8") as output_file:
        for morpheme_line in morphemes_file:
            morpheme_line = morpheme_line.strip()
            target_morphemes = morpheme_line.split()  # Lista de morfemas alvo
            matched_segments = []
            remaining_morphemes = target_morphemes.copy()

            for segment in lexicon.keys():
                segment_morphemes = segment.split()  # Lista de morfemas do segmento
                i = 0
                j = 0
                while i < len(remaining_morphemes) and j < len(segment_morphemes):
                    if remaining_morphemes[i] == segment_morphemes[j]:
                        matched_segments.append(remaining_morphemes[i])
                        i += 1
                        j += 1
                    else:
                        j += 1  # Avança para o próximo morfema do segmento

                # Remove os morfemas correspondentes da lista remaining_morphemes
                for morpheme in matched_segments:
                    if morpheme in remaining_morphemes:
                        remaining_morphemes.remove(morpheme)

            # Verifica se todos os morfemas da linha alvo foram encontrados na ordem correta
            if len(target_morphemes) == len(matched_segments) and target_morphemes == matched_segments:
                output_file.write(f"Linha alvo: '{morpheme_line}' - Segmentos correspondentes: '{' '.join(matched_segments)}' (com {len(matched_segments)} palavras em comum)\n")
                best_matches_found += 1
            else:
                output_file.write(f"Linha alvo: '{morpheme_line}' - Nenhuma correspondência encontrada\n")
            total_morphemes += 1

    return best_matches_found, total_morphemes
