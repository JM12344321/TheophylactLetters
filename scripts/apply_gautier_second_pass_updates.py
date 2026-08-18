from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = ROOT / "revised_second_pass" / "letters"
MANIFEST = ROOT / "02_sources" / "gautier" / "letter_packets" / "packet_manifest.json"


def set_line(text: str, label: str, value: str) -> str:
    pattern = rf"^({re.escape(label)}:\s*).*$"
    replacement = rf"\g<1>{value}"
    return re.sub(pattern, replacement, text, flags=re.MULTILINE)


def ensure_after_line(text: str, anchor_label: str, new_label: str, value: str) -> str:
    if re.search(rf"^{re.escape(new_label)}:\s*", text, flags=re.MULTILINE):
        return set_line(text, new_label, value)
    pattern = rf"^({re.escape(anchor_label)}:\s*.*)$"
    return re.sub(pattern, rf"\1\n{new_label}: {value}", text, count=1, flags=re.MULTILINE)


def replace(text: str, old: str, new: str, gid: str, warnings: list[str]) -> str:
    if old not in text:
        warnings.append(f"{gid}: did not find expected text: {old[:80]!r}")
        return text
    return text.replace(old, new, 1)


def replace_section(text: str, heading: str, next_heading: str, body: str, gid: str, warnings: list[str]) -> str:
    pattern = rf"({re.escape(heading)}\n\n).*?(\n\n{re.escape(next_heading)})"
    replacement = rf"\1{body}\2"
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        warnings.append(f"{gid}: did not replace section {heading!r}")
    return new_text


def remove_unresolved_checkboxes(text: str) -> str:
    return re.sub(
        r"## Unresolved Issues\n\n- \[ \] .*?\n\n## Audit Trail",
        "## Unresolved Issues\n\n- None material for the translated text.\n\n## Audit Trail",
        text,
        count=1,
        flags=re.S,
    )


def main() -> None:
    manifest = {row["gautier_id"]: row for row in json.loads(MANIFEST.read_text(encoding="utf-8"))}
    warnings: list[str] = []

    for n in range(1, 136):
        gid = f"G{n:03d}"
        path = LETTERS / gid / "translation_v2.md"
        if not path.exists():
            warnings.append(f"{gid}: missing translation_v2.md")
            continue

        text = path.read_text(encoding="utf-8")
        info = manifest[gid]
        text = set_line(text, "- Gautier page range", info["citation"])
        text = ensure_after_line(text, "- Gautier page range", "- Gautier source packet", info["packet"])
        text = set_line(text, "- Identification confidence", "high")

        text = text.replace(
            "Second-pass status: baseline_first_pass_copied_pending_clause_audit",
            "Second-pass status: baseline_first_pass_gautier_packeted_pending_full_clause_audit",
        )
        text = text.replace("needs_gautier_collation", "needs_full_clause_audit")
        text = text.replace(
            "- Source condition: pg_ocr_not_collated",
            "- Source condition: gautier_packet_available_pending_full_clause_audit",
        )
        text = text.replace(
            "- Source condition: damaged_or_corrupt_ocr",
            "- Source condition: gautier_packet_available_ocr_sensitive_pending_full_clause_audit",
        )
        text = text.replace(
            "- Source condition: merged_or_continuation_packet",
            "- Source condition: gautier_packet_available_boundary_sensitive_pending_full_clause_audit",
        )
        text = text.replace(
            "- Source condition: gibi_parallel_text_only",
            "- Source condition: gautier_packet_available_from_cfHB_pending_full_clause_audit",
        )

        path.write_text(text, encoding="utf-8")

    upgrades = {
        "G004": ("gautier_collated_targeted_lexical_revision", "B", "gautier_collated_complete_targeted_sections"),
        "G007": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G009": ("gautier_packeted_no_full_clause_audit", "C", "gautier_packet_available_pending_full_clause_audit"),
        "G010": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G019": ("gautier_collated_technical_terms_corrected", "A", "gautier_collated_complete"),
        "G023": ("gautier_collated_legal_term_corrected", "A", "gautier_collated_complete"),
        "G040": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G041": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G047": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G050": ("gautier_collated_lexical_correction", "A", "gautier_collated_complete"),
        "G056": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G069": ("gautier_collated_negation_and_ending_corrected", "A", "gautier_collated_complete"),
        "G091": ("gautier_collated_short_letter_corrected", "A", "gautier_collated_complete"),
        "G093": ("gautier_collated_short_letter_corrected", "A", "gautier_collated_complete"),
        "G094": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G101": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G102": ("gautier_collated_homeric_quote_corrected", "A", "gautier_collated_complete"),
        "G103": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G107": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G109": ("gautier_collated_opening_corrected", "A", "gautier_collated_complete"),
        "G110": ("gautier_collated_targeted_corrections", "B", "gautier_collated_complete_targeted_sections"),
        "G111": ("gautier_collated_lacuna_and_property_terms_checked", "B", "gautier_collated_minor_lacuna"),
        "G114": ("gautier_collated_negation_corrected", "A", "gautier_collated_complete"),
        "G115": ("gautier_collated_difficult_name_reading_checked", "B", "gautier_collated_localized_uncertainty"),
        "G116": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G117": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G122": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G124": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G126": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G128": ("gautier_collated_daylight_correction", "A", "gautier_collated_complete"),
        "G130": ("gautier_collated_short_letter_checked", "A", "gautier_collated_complete"),
        "G131": ("gautier_collated_short_letter_corrected", "A", "gautier_collated_complete"),
        "G132": ("gautier_collated_short_consolation_checked", "B", "gautier_collated_complete_prosopography_uncertain"),
        "G133": ("gautier_collated_short_consolation_corrected", "B", "gautier_collated_complete_prosopography_uncertain"),
        "G135": ("gautier_collated_christological_fragment_reassigned", "B", "gautier_collated_complete_surviving_excerpt"),
    }
    for gid, (status, confidence, source_condition) in upgrades.items():
        path = LETTERS / gid / "translation_v2.md"
        text = path.read_text(encoding="utf-8")
        text = set_line(text, "Second-pass status", status)
        text = set_line(text, "Confidence category", confidence)
        text = set_line(text, "- Source condition", source_condition)
        path.write_text(text, encoding="utf-8")

    edits: dict[str, list[tuple[str, str]]] = {
        "G004": [
            (
                "Coming down from the district of Panteichion, that squall made the crossing impassable unless we were to put in at Apollonias",
                "Coming down from the district of Panteichion, that brisk and violent wind made the crossing impassable unless we were to put in at Apollonias",
            )
        ],
        "G109": [
            (
                "You do Athenian things, and we are so hated by you that you do not even address us.",
                "You behave toward us as the Mycenaeans did toward Orestes, and we are so hated by you that you do not even address us.",
            )
        ],
        "G019": [
            (
                "They are still dragged into billeting obligations and bread-fines, even though the chrysobull commanded that they be above both these dirty public services and the bread-fines.",
                "They are still dragged into local guard services and food-supply obligations, even though the chrysobull commanded that they be exempt from both these sordid public services and the food-supply obligations.",
            )
        ],
        "G023": [
            (
                "The whole army, if questioned, will make the truth of the case plain.",
                "The strategos, once questioned, will make the truth of the case plain.",
            )
        ],
        "G050": [
            (
                "Thus I am useless and talkative beyond what is fitting.",
                "Thus I am excessive and talkative beyond what is fitting.",
            )
        ],
        "G069": [
            (
                "But so that you may not appear to be that much-devising son of Laertes, and so that you may have reason as the opponent of evil, Hermes, giving you the moly, has surely already explained everything well to you.",
                "See to it, then, that you appear to me as that much-devising son of Laertes and that you have reason as the opponent of evil. Hermes, giving you the moly, has surely already explained everything well to you.",
            ),
            (
                "Do not worry, then.",
                "Do not delay, then.",
            ),
            (
                "Perhaps I may even sing victory-songs for you, not at all less honorable than those of Bacchylides and Simonides, perhaps even fitted to the Boeotian lyre, and certainly [...]",
                "Perhaps I may even sing victory-songs for you, not at all less honorable than those of Bacchylides and Simonides, perhaps even fitted to the Boeotian lyre, and certainly having a more splendid theme and being recited on a more solemn platform.",
            ),
        ],
        "G091": [
            (
                "My lord and son, if you yourself were holding a water jar in both hands, would you pour it over burning limbs, or would you pass by after looking on with proud or unfeeling eyes?",
                "Most honored son in the Lord, if you saw me burning and were yourself holding a water jar in both hands, would you pour it over burning limbs, or would you pass by after looking on with proud or unfeeling eyes?",
            )
        ],
        "G093": [
            (
                "Show that you can heal.",
                "Show us, then, how much you can do.",
            )
        ],
        "G102": [
            (
                "\"Stranger, move away from tyrants' feet, lest the scepter and thought of God not help you.\"",
                "\"Stranger, stand aside, out of the tyrants' way, lest the scepter and garland of the god not help you.\"",
            )
        ],
        "G110": [
            (
                "which you, the new Israel, have pitched while wandering through the desert on your account.",
                "which you, the new Israel, have pitched while wandering through our desert.",
            ),
            (
                "and because the river tolls are badly disappearing, it has no bridge.",
                "and because of the accursed river tolls, it has no bridge.",
            ),
        ],
        "G111": [
            (
                "In Thessalonica, fullness is expected for me; in the churches apart from the archbishopric, emptiness.",
                "In Thessalonica, fullness is expected for me; at the Churches, a chorion of the archbishopric, emptying.",
            )
        ],
        "G114": [
            (
                "You are not the cause of trouble for me.",
                "You are the cause of troubles for me.",
            )
        ],
        "G115": [
            (
                "But do you wish me to give a rule? We lie beneath the brows of cheerfulness - or rather beneath whatever way they may incline; where they incline, the man always meeting them knows.",
                "Do you wish me to give another rule? We lie beneath the brows of Euphemianos: wherever they nod, that way we are carried; in what direction they nod, anyone who has ever met him knows.",
            )
        ],
        "G126": [
            (
                "we have obtained moderate rest, at least in the few things remaining to the Church around Ohrid.",
                "we have obtained moderate rest, at least in the meager properties left to the Church of Achrida.",
            ),
            (
                "charming our tax official",
                "charming our praktor",
            ),
            (
                "the aims of the tax officials",
                "the aims of the praktores",
            ),
        ],
        "G128": [
            (
                "For now, composing this little letter for you by lamplight, I had no way to take the medicine from the box.",
                "For now, composing this little letter for you in daylight, I had no way to take the medicine from the box.",
            )
        ],
        "G130": [
            (
                "for I infer that you have affairs in hand beneath which there is some profit.",
                "for I infer that you have affairs in hand in which there is also some profit.",
            )
        ],
        "G131": [
            (
                "Write to me, then, more plainly: whether you are in certain things, and whether they are worthy of the hopes on which we were nourished.",
                "Write to me, then, more plainly: what condition you are in, and whether it is worthy of the hopes on which we were nourished.",
            )
        ],
        "G133": [
            (
                "Having learned of the sickness that has come upon you, my much-loved and good brother, and not knowing to what end it will bring you, grief sinks my reasoning into the depths;",
                "Having learned of the sickness that has come upon you, my much-loved and good brother, and not knowing to what end it will bring you, I am wounded in soul; grief sinks my reasoning into the depths;",
            )
        ],
    }
    for gid, pairs in edits.items():
        path = LETTERS / gid / "translation_v2.md"
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            text = replace(text, old, new, gid, warnings)
        path.write_text(text, encoding="utf-8")

    section_replacements = {
        "G004": (
            "- Corrected the meteorological phrase governed by Gautier's Greek adjective for a strong/bright wind: not literal \"bright,\" but a brisk and violent wind in context; the previous v2 note overidentified the word as a storm noun.",
            "- Gautier's text confirms the nautical passage and the closing blessing as substantially complete; the lexical issue is limited to the force of the wind adjective in context.\n- The \"Bulgarians\" passage is intentionally sharp and comic. I have preserved its unpleasant force rather than smoothing it into neutral complaint.",
            "- [ ] Final expert audit may revisit the rendering of the wind adjective in context; no larger lacuna is visible in Gautier.",
        ),
        "G007": (
            "- Checked the whole short companion letter against Gautier; no material semantic correction required.",
            "- Gautier confirms that this letter points to G005 and G006 as companion accounts of Theophylact's troubles.\n- The addressee is Niketas, didaskalos of the Great Church and nephew of the metropolitan of Serres.",
            "- None material for the translated text.",
        ),
        "G010": (
            "- Checked the whole short exhortation against Gautier; no material semantic correction required.",
            "- Gautier identifies the recipient as John Komnenos, son of the sebastokrator Isaac and doux of Dyrrachion.\n- The letter uses Scripture's protective language, \"wall and rampart,\" for the recipient.",
            "- None material for the translated text.",
        ),
        "G019": (
            "- Corrected the administrative terms: `paramonai` are local guard services here, and `psomozemiai` are food-supply obligations, not bread-fines.",
            "- Gautier prints this as an independent short letter and identifies the recipient as John Komnenos, son of the sebastokrator.\n- The appeal concerns priests of Pologos and exemptions confirmed by chrysobull.",
            "- None material for the translated text.",
        ),
        "G023": (
            "- Corrected `strategos`: the witness to be questioned is the strategos, not \"the whole army.\"",
            "- The letter asks that an already adjudicated lawsuit not be reopened.\n- Gautier's notes preserve uncertainty about Makrembolites' exact identification, but the translated legal action is clear.",
            "- None material for the translated text.",
        ),
        "G040": (
            "- Checked the whole recommendation letter against Gautier; no material semantic correction required.",
            "- The letter commends the newly burdened bishop Glabenitzes to Niketas Polites.\n- The Koprinista/dung-heap joke is kept because Gautier's note confirms the Heracles/Augean-stables play.",
            "- None material for the translated text.",
        ),
        "G041": (
            "- Checked the whole consolation letter against Gautier; no material semantic correction required.",
            "- The letter consoles Anemas over an unrealized meeting by privileging intellectual/spiritual presence over bodily presence.\n- Theophylact deliberately replaces pagan fate language with biblical providence.",
            "- None material for the translated text.",
        ),
        "G047": (
            "- Checked the whole Mermentopoulos letter against Gautier and confirmed it as the source that had been duplicated into the old G006 slot.",
            "- This is a playful complaint that the addressee's eloquence benefits everyone except Theophylact.\n- The ending alludes to Homeric rescue imagery; weak resources can still be saved by a powerful ally.",
            "- None material for the translated text.",
        ),
        "G050": (
            "- Corrected `περιττός` from \"useless\" to \"excessive\" in the self-mocking sentence.",
            "- \"Donkeys hear a lyre\" is the governing insult: Theophylact's learning is wasted on his local audience.\n- Leibethra, associated with the Muses/Orpheus, is used ironically for Achrida.",
            "- None material for the translated text.",
        ),
        "G056": (
            "- Checked the whole short appeal to the bishop of Semna against Gautier; no material semantic correction required.",
            "- The altered quotation is Romans 13:4 turned bitterly against oppressive fiscal officials.",
            "- None material for the translated text.",
        ),
        "G069": (
            "- Removed an unsupported negative in the Odysseus comparison: Theophylact urges the addressee to appear like the resourceful son of Laertes.\n- Corrected \"do not worry\" to \"do not delay.\"\n- Restored the complete ending from Gautier instead of leaving an OCR-clipped bracket.",
            "- The Homeric imagery is from Odysseus' encounters and Hermes' moly in Odyssey 10.\n- The athletic close invokes Bacchylides, Simonides, and Pindar's Boeotian lyre.",
            "- None material for the translated text.",
        ),
        "G091": (
            "- Restored the opening condition \"if you saw me burning,\" which had been compressed out of the first-pass English.",
            "- Gautier identifies the addressee probably as Niketas, didaskalos of the Great Church.\n- The opening image asks the addressee to relieve urgent suffering, not merely to understand it.",
            "- None material for the translated text.",
        ),
        "G093": (
            "- Corrected the final request from the over-specific \"show that you can heal\" to \"show us how much you can do.\"",
            "- Gautier's printed ending is complete; the old OCR damage note is superseded.\n- The Zeus/thunderbolt joke is a playful classicizing compliment to the imperial physician's proximity to power.",
            "- None material for the translated text.",
        ),
        "G094": (
            "- Checked the whole Alcmaeon/Achelous appeal against Gautier; no material semantic correction required.",
            "- Alcmaeon found refuge on newly formed land, often associated with Achelous; Theophylact recasts that myth as a plea for safe standing ground.\n- The fiscal officer/executioner wordplay is deliberately retained.",
            "- None material for the translated text.",
        ),
        "G101": (
            "- Checked the whole short letter against Gautier; no material semantic correction required.",
            "- The letter uses the Gospel story of Legion and the swine to describe an uncorrected opponent.\n- Gautier's note suggests the opponent is probably a praktor such as Iasites, or possibly Lazaros.",
            "- None material for the translated text.",
        ),
        "G102": (
            "- Corrected the Homeric warning: `στέμμα θεοῖο` is the god's garland, not \"thought of God.\"",
            "- The advice to Michael is courtly and pastoral: humility, caution, and diligent medical service in the palace.\n- Gautier identifies the occasion as Michael Pantechnes' entry into imperial medical service.",
            "- None material for the translated text.",
        ),
        "G109": (
            "- Corrected the opening comparison from unsupported \"Athenian things\" to the Mycenaeans' treatment of Orestes.\n- Gautier confirms Tornikios as Theophylact's son-in-law through his niece and explains the likely military-camp leave request.",
            "- The letter asks for Tornikios to be released from a military-camp obligation.\n- The opening alludes to Euripides' Orestes, as Gautier notes.",
            "- None material for the translated text.",
        ),
        "G110": (
            "- Corrected two Gautier-controlled details: the army moves through Theophylact's desert, not a desert \"on your account\"; the bridge problem is due to accursed river tolls, not tolls \"disappearing.\"",
            "- The letter explains why illness and the flooded Axios/Vardar prevent Theophylact from traveling.\n- The skiff/Acheron joke is both comic and anxious: the crossing is dangerous.",
            "- [ ] Final expert audit should revisit the long river-crossing sentence and the exact form Bardouarios/Bardarion.",
        ),
        "G111": (
            "- Corrected the property phrase: `the Churches` is a chorion of the archbishopric, not churches apart from it.\n- Preserved Gautier's small opening lacuna rather than supplying a verb silently.",
            "- \"Medicine through viper flesh\" likely refers to theriac.\n- The house/estate language opposes filling the Thessalonican house with occupiers and emptying the chorion called the Churches.",
            "- [ ] Gautier marks a small lacuna near the opening; property details still need historical annotation.",
        ),
        "G114": (
            "- Corrected a lost negation: Theophylact says Pantechnes is the cause of his troubles, not that he is not the cause.\n- Gautier confirms the title proximos and the letter's complete ending.",
            "- This is a recommendation letter whose force depends on the opening joke: Pantechnes' influence makes Theophylact a target for petitioners.\n- `Proximos` is retained as a Byzantine court title.",
            "- None material for the translated text.",
        ),
        "G115": (
            "- Corrected the difficult brows sentence from abstract \"cheerfulness\" to Gautier's proposed proper name Euphemianos.",
            "- Gautier treats the addressee as uncertain and the name Euphemianos as a cautious proposal from a difficult abbreviation.\n- The final sentence alludes to Christ's proclamation of release to captives in Hades.",
            "- [ ] The reading Euphemianos and the exact force of the brows joke remain localized uncertainties.",
        ),
        "G122": (
            "- Checked against Gautier II, letter 122; no material semantic correction made.\n- Corrected the see to Debre, a suffragan of Achrida, rather than leaving the Deabolis/Debar doublet unresolved.",
            "- This is another short bereavement letter after the death of Theophylact's brother Demetrios.\n- The final request urges the bishop to return to his see.",
            "- None material for the translated text.",
        ),
        "G124": (
            "- Checked the whole short note against Gautier II, letter 124; no material semantic correction required.",
            "- A very short illness note asking the former chartophylax Nikephoros for prayers.\n- Gautier preserves a minor variant in the final line, but it does not affect the English sense.",
            "- None material for the translated text.",
        ),
        "G126": (
            "- Checked against Gautier II, letter 126 and retained the charm/incantation metaphor.\n- Standardized `praktor` rather than modernizing the fiscal office as tax official.\n- Corrected the opening property phrase to the meager properties left to the Church of Achrida.",
            "- Gautier identifies the addressee as the sebastos George Palaiologos and the praktor probably as Iasites.\n- The desert/serpent language makes an administrative request rhetorically biblical.",
            "- None material for the translated text.",
        ),
        "G128": (
            "- Corrected \"by lamplight\" to \"in daylight\" for Gautier's `ὑπὸ φωτί`.\n- Checked the phoenix/resurrection consolation against Gautier.",
            "- The closing is not damaged in Gautier; it moves from winter/spring to the phoenix and then to a more divine Christian resurrection hope.",
            "- None material for the translated text.",
        ),
        "G130": (
            "- Checked the whole short note against Gautier and corrected the idiom \"in which there is also some profit.\"",
            "- The letter turns silence into a hopeful inference: no news may mean profitable busyness.",
            "- None material for the translated text.",
        ),
        "G131": (
            "- Corrected the final request: Theophylact asks what condition the addressee is in, not whether he is \"in certain things.\"",
            "- Gautier's short text is complete and identifies the addressee as the same Michael Pantechnes sequence.",
            "- None material for the translated text.",
        ),
        "G133": (
            "- Restored the omitted opening clause \"I am wounded in soul.\"\n- Checked the prayer for recovery against Gautier's Greek.",
            "- Gautier rejects the manuscript's non-original superscription and treats the correspondent as unnamed, probably Demetrios.\n- The translation keeps the affective intensity without inserting the probable identification into the body text.",
            "- [ ] The addressee remains a prosopographical uncertainty; no textual lacuna affects the translated body.",
        ),
        "G135": (
            "- Reassigned the Tivanios/Tigranes Armenian fragment from old local G134 to Gautier G135.\n- Tightened the iron analogy by translating the shape adjective as \"elongated and blade-like.\"\n- Corrected the confused-union sentence from \"neither the one nor the other\" to \"not one rather than the other,\" matching Gautier's Greek.",
            "- Corrected corpus identity: the Tivanios/Tigranes Armenian Christological excerpt is G135, not G134.\n- Subject: natures and wills of Christ; iron/fire analogy.\n- Gautier's printed excerpt continues through the final iron/fire sentence; the local PG OCR break is superseded by the Gautier packet.",
            "- [ ] Verify whether Tibanios should be identified with Tigranes in final prosopography; the translated excerpt itself is complete as preserved by Gautier.",
        ),
    }
    for gid, (changes, notes, unresolved) in section_replacements.items():
        path = LETTERS / gid / "translation_v2.md"
        text = path.read_text(encoding="utf-8")
        text = replace_section(text, "## Consequential Changes From First Pass", "## Source And Revision Notes", changes, gid, warnings)
        text = replace_section(text, "## Source And Revision Notes", "## Unresolved Issues", notes, gid, warnings)
        text = replace_section(text, "## Unresolved Issues", "## Audit Trail", unresolved, gid, warnings)
        path.write_text(text, encoding="utf-8")

    for gid in ["G103", "G107", "G116", "G117"]:
        path = LETTERS / gid / "translation_v2.md"
        text = path.read_text(encoding="utf-8")
        text = remove_unresolved_checkboxes(text)
        path.write_text(text, encoding="utf-8")

    if warnings:
        print("\n".join(warnings))


if __name__ == "__main__":
    main()
