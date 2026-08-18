from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = ROOT / "revised_second_pass" / "letters"
TODAY = "2026-08-18"


def replace_required(text: str, old: str, new: str, gid: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"{gid}: expected text not found: {old[:80]!r}")
    return text.replace(old, new)


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = rf"(## {re.escape(heading)}\n\n)(.*?)(?=\n## |\Z)"
    replacement = rf"\1{body.strip()}\n"
    new_text, count = re.subn(pattern, replacement, text, flags=re.S)
    if count != 1:
        raise RuntimeError(f"section {heading!r} not replaced cleanly")
    return new_text


def set_line(text: str, prefix: str, value: str) -> str:
    pattern = rf"^{re.escape(prefix)}.*$"
    new_text, count = re.subn(pattern, f"{prefix}{value}", text, flags=re.M)
    if count != 1:
        raise RuntimeError(f"line {prefix!r} not replaced cleanly")
    return new_text


UPDATES: dict[str, dict] = {
    "G009": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Standardized `kanonikon` rather than flattening the fiscal/ecclesiastical due.",
            "Corrected the final theological repayment clause: the addressee will have God as legislator and rewarder, not merely an abstract comparison discovered by the translator.",
        ],
        "notes": [
            "Checked against Gautier II, letter 9.",
            "The letter concerns the Caesar's order about the kanonikon and Theophylact's rhetoric of being defeated by benefaction.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "But now the command concerning the canonical payment has been added to those earlier gifts.",
                "But now the command concerning the kanonikon has been added to those earlier gifts.",
            ),
            (
                "I have found God greater in the matter of ecclesiastical offerings, commanding all to complete the two-drachma payment of their subjection, and preparing rewards for goodness both here and there. Him alone you will not be able to surpass, whatever devices you contrive. Rather, the more you conquer us, the more you will be conquered by him, or rather conquered infinitely more by his acts of generosity.",
                "You will have God, the legislator of ecclesiastical matters, who commands all to fulfill their submission to him by paying the didrachmon, giving the rewards of goodness both here and there. Him alone you will not be able to surpass, whatever devices you contrive. Rather, the more you conquer us, the more you will be conquered by him, or rather conquered infinitely more by his acts of generosity.",
            ),
        ],
    },
    "G013": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the Theotokos from Theophylact's guardian to the addressee's guardian.",
            "Followed Gautier's `strougai` emendation: the fish shortage is tied to fish-channels, not small birds.",
        ],
        "notes": [
            "Checked against Gautier II, letter 13.",
            "Gautier explicitly rejects the manuscript `strouthon` reading and prints `strougon`; the translation preserves the technical note in English.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "Since it is the season of fasting and of eating fish, my guardian the Theotokos sends your majesty a blessing: two hundred little salted fish. To the poor she is poor in fish because of the lack of small birds, but she is rich in the protection which she always asks for your majesty.",
                "Since it is the season of fasting and of eating fish, your guardian, the Theotokos, sends your majesty a blessing: two hundred little salted fish. She is poor in fish because of the loss of the strougai, the fish-channels, but rich in the protection which she always asks for your majesty.",
            ),
        ],
    },
    "G016": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Removed a false damaged-phrase marker in the closing sentence.",
            "Corrected the exhortation: the addressee is to profit from the letter according to faith and relax both labor and threat for subordinates.",
        ],
        "notes": [
            "Checked against Gautier II, letter 16.",
            "The closing alludes to Ephesians 6:9 on masters giving up threats.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "Yet since all things are possible to the one who believes, take thought for my affairs just as you have believed. I know, moreover, that the words friends cry out beneath runners become wings to them.\n\nMay God, who benefits us from every side, for he made all things very good, grant you benefit that is true life-benefit [a damaged phrase intervenes], not only in deed but also in threat, as the great Apostle commanded.",
                "Yet since all things are possible to the one who believes, may you profit from my letter in the measure of your faith. I know, moreover, that the words friends cry out beneath runners become wings to them.\n\nMay God, who benefits us from every side, for he made all things very good, grant you both to be benefited and to benefit, by relaxing for those under your hand not only the work but also the threat, as the great Apostle commanded.",
            ),
        ],
    },
    "G020": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the opening rhetorical question from self-deprecation to blessedness at benefiting a great soul."],
        "notes": [
            "Checked against Gautier II, letter 20.",
            "The letter uses the Gospel parable of the minas/talents and identifies the word as the Master's coin.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "Who are we, my most blessed and most illustrious lord, if we are of any use to so great a soul?",
                "Who is more blessed than we, my most illustrious lord, if we should benefit so great a soul?",
            ),
        ],
    },
    "G021": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected `kainismos` as a change in affairs, not a sting.",
            "Restored the Kritopouloi as the protected party; they are not generic judges.",
            "Clarified `episkeptitai` as a technical office rather than flattening it to inspectors only.",
        ],
        "notes": [
            "Checked against Gautier II, letter 21.",
            "Gautier notes that Demetrios here is Demetrios Kritopoulos, not Theophylact's brother.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "I have learned, most honored brother, that there has now been some sting in the affairs concerning us:",
                "I have learned, most honored brother, that there has now been some change in the affairs concerning us:",
            ),
            (
                "Since these things have happened in this way, and since the judges are mine, I write to your sacredness so that they may be guided by you as much as possible, and especially Demetrios.",
                "Since these things have happened in this way, and since the Kritopouloi are mine, I write to your sacredness so that they may be guided by you as much as possible, and especially Demetrios.",
            ),
            (
                "Assist them, then, even if you meet them only as they are already going forward.",
                "Assist them, then, if anything rough should confront them.",
            ),
            (
                "Let the inspectors also be guided by you in all things.",
                "Let the episkepititai also be guided by you in all things.",
            ),
        ],
    },
    "G024": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the petition so Theophylact himself beseeches the powerful patron.",
            "Corrected repeated `ekbole` language: the issue is the levy/dispatch of infantrymen, not expulsion.",
            "Corrected the Theotokos clause: the addressee gives to her whatever he gives to Theophylact's church.",
        ],
        "notes": [
            "Checked against Gautier II, letter 24.",
            "The administrative object is the infantry levy from Achrida, with the smallness of the theme as the central argument.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "Therefore I shall write for those entrusted to me, and they will ask from the very heart of the one who is able to have mercy.",
                "Therefore I shall speak and write for those entrusted to me, and I shall beseech from the very heart, as they say, the one who is able to have mercy.",
            ),
            ("expulsion of foot-soldiers", "levy of infantrymen"),
            ("those who have been expelled from here", "those levied from here"),
            ("The foot-soldiers already expelled are enough to crush us.", "The infantrymen already levied are enough to crush us."),
            ("Let the expulsion go no further", "Let the levy go no further"),
            ("those already expelled have sufficiently brought about", "those already levied have sufficiently brought about"),
            (
                "May the Theotokos, to whom we belong and who gives us everything by her works, grant you an unimpeded relation toward God and an unconquered stance toward enemies",
                "May the Theotokos, to whom we belong and to whom you give everything that you give to us, grant you an unimpeded relation toward God and an unconquered stance toward enemies",
            ),
        ],
    },
    "G025": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_localized_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Removed unsupported `holy antidote` language from the thanksgiving sentence.",
            "Made the difficult throat-sound joke more literal and less architecturally inventive.",
        ],
        "notes": [
            "Checked against Gautier II, letter 25.",
            "The clause around `pareptysas` and the long throat-sounds remains rhetorically difficult; Gautier notes a possible correction.",
        ],
        "unresolved": ["The exact nuance of the throat-sound joke should be revisited in a final scholarly audit."],
        "replacements": [
            (
                "and if you spat aside any long throat-noises, on which many pride themselves, you built for yourself a higher sacred precinct.",
                "and even if you let slip some long throat-sound, on which many pride themselves, you did so after pitching it high.",
            ),
            (
                "I in turn will give you thanksgiving for these things as a holy antidote. And if the flavor from your honey is more musical and sweeter than now, so much the better.",
                "I in turn will repay you with thanksgiving for these things. And if that thanksgiving is more musical and sweeter than now, that will be the juice drawn from your honey.",
            ),
        ],
    },
    "G026": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_property_term_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected `praktikon`, `praktor`, `ospetion`, `aule`, and `zeugologion` terminology.",
            "Changed the courtyard language to a farm/farmyard sense, following Gautier's note on `aule`.",
        ],
        "notes": [
            "Checked against Gautier II, letter 26.",
            "The property/fiscal vocabulary is technical and should be checked against Byzantine fiscal scholarship in the final audit.",
        ],
        "unresolved": ["Precise legal force of `douleia` and `aule` remains localized B-level uncertainty."],
        "replacements": [
            ("subject to no practical exaction", "not entered in a praktikon"),
            (
                "Then, finding it under a small servitude by the collector of the day, I held it, like many others, under that slight consolation.",
                "Then, finding it under a small douleia from the current praktor as a slight consolation, I held it, like many others.",
            ),
            ("the Church's lodging-house and courtyard", "the Church's ospetion and aule, its house and farmyard"),
            ("concerning the courtyard", "concerning the aule"),
            ("both the land and the courtyard", "both the land and the aule"),
        ],
    },
    "G028": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the Demetrios/Smyrnaios pedagogical appeal against Gautier; no material correction required."],
        "notes": [
            "Checked against Gautier II, letter 28.",
            "The `beautiful fools` phrase alludes to Proverbs 9 and is intentionally playful.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G030": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_monastery_name_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected the Charybdis/camp phrase.",
            "Replaced unsupported `holy men of Serres` with Gautier's conjectural Hagiosergitai.",
        ],
        "notes": [
            "Checked against Gautier II, letter 30.",
            "Gautier rejects the manuscript form as impossible and conjectures Hagiosergitai, probably a Saint Sergius monastic reference.",
        ],
        "unresolved": ["The Hagiosergitai name remains conjectural and should be revisited with the apparatus/manuscripts."],
        "replacements": [
            (
                "for even now I have measured out [a whole Charybdis] and worn down the camp,",
                "for even now I have crossed deadly Charybdis and spent time in the military camp,",
            ),
            ("As for the holy men of Serres,", "As for the Hagiosergitai,"),
        ],
    },
    "G032": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_name_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected the Euripidean opening.",
            "Restored the technical title `katepano` and the dust-winnowing image.",
            "Corrected the third oppressor from `Destroyer` to a Pharaoh-related name joke.",
            "Corrected the Church property term from poor-house to poor little property.",
        ],
        "notes": [
            "Checked against Gautier II, letter 32.",
            "The letter has dense comic and administrative wordplay; some proper-name identifications remain uncertain.",
        ],
        "unresolved": ["The Pharaoh-related name joke and some official identifications remain B-level uncertainties."],
        "replacements": [
            (
                "How sweetly a friend's word came to me at the proper moment: a charm, a helper against sickness. These are Orestes' words, as you know, my dearest head; I parody them slightly and speak them of you. Shall I add the words of the comic poet too: how glad I am, how delighted, how I wish to dance?",
                "Dear charm of speech, helper against sickness, how sweetly you came to me at the proper moment. These are Orestes' words, as you know, my dearest head; I parody them slightly and speak them of you. Shall I add the words of the comic poet too: how glad I am, how delighted, how I wish to dance?",
            ),
            (
                "now the one who strangles was bringing plague even upon the mind.",
                "now the katepano was winnowing even the dust.",
            ),
            (
                "If there was some third evil among them, what remains but the Destroyer? From his very name I do not know whether he is in any way more tolerable than those already mentioned.",
                "There was also some third man among them, akin to Pharaoh at least by name. I do not know whether he is in any way more tolerable than those already mentioned.",
            ),
            ("the Church's poor-house", "the Church's poor little property"),
        ],
    },
    "G033": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the healing-plaster paraphrase to the musical/incantatory contrast required by the Greek."],
        "notes": [
            "Checked against Gautier II, letter 33.",
            "The golden-wand passage alludes to Iliad 24.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "If we are fortunate, write in song; if unfortunate, write as one who applies healing plaster to the fall.",
                "If we are fortunate, write to sing along; if unfortunate, write to charm our grief away with song.",
            ),
        ],
    },
    "G034": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the cure sentence: Theophylact says he is far from contriving a cure, not that a costly cure must be contrived.",
            "Corrected `private men` to `those who know` in the irony sentence.",
        ],
        "notes": [
            "Checked against Gautier II, letter 34.",
            "The letter preserves the Bulgaria/rusticity contrast and allusions to Proverbs, Song of Songs, Echo, Tantalus, and Ecclesiastes.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            ("Some cure, indeed, must be contrived at great cost.", "I am far indeed from contriving any cure."),
            ("But you should not pamper yourself by speaking ironically toward private men.", "But you should not pamper yourself by playing the ironist before those who know."),
        ],
    },
    "G043": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the Jacob's-ladder ascent and stone/foe comparison against Gautier; no material correction required."],
        "notes": ["Checked against Gautier II, letter 43."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G044": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the love/letters/Jacob's-ladder argument and the admonition about lay and ecclesiastical order against Gautier."],
        "notes": [
            "Checked against Gautier II, letter 44.",
            "The closing admonition depends on the distinction between the order that initiates and the order that is initiated.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G046": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_classical_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected the cooking/meteorological example: frying, roasting, and boiling, not flying.",
            "Standardized Sarambos spelling.",
        ],
        "notes": [
            "Checked against Gautier II, letter 46.",
            "Gautier notes that the Sarambos sentence is not fully clear; confidence remains B.",
        ],
        "unresolved": ["Sarambos/Plato-Gorgias sentence still needs expert review."],
        "replacements": [
            ("condensation, roasting, and flying", "frying, roasting, and boiling"),
            ("Sarabos", "Sarambos"),
        ],
    },
    "G048": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked illness, Glavenitza/Vidin/Slanitza arrows, and Paieon/Machaon/Podaleirios allusions against Gautier."],
        "notes": ["Checked against Gautier II, letter 48."],
        "unresolved": ["None material for the translation."],
        "replacements": [("Glabenitza", "Glavenitza")],
    },
    "G049": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the Autolykos/Odysseus joke: John rejects the name `negligent`, not his calling.",
            "Preserved `dikaiomata` as a technical rights/claims term.",
        ],
        "notes": ["Checked against Gautier II, letter 49."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "For I was always accusing you of negligence and saying that you disowned your calling, as though even Autolykos would not disown Odysseus.",
                "For I was always accusing you as negligent, and you were always rejecting the name, as Autolykos would not have rejected Odysseus.",
            ),
            ("that you not also lose the rights that were given to you.", "that you not also lose the dikaiomata granted to you."),
        ],
    },
    "G051": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Removed the false PG/OCR break marker; Gautier prints a complete short letter."],
        "notes": ["Checked against Gautier II, letter 51."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "he may keep us free from the night of evil deeds [the PG/OCR packet breaks off here].",
                "he may keep us free from the night of evil deeds.",
            ),
        ],
    },
    "G064": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected a false negative: the bishop is grateful after receiving the letters, not without receiving them."],
        "notes": ["Checked against Gautier II, letter 64."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "Yet even without receiving what he asked, he has gratitude and rejoices wonderfully.",
                "And indeed, having received them, he is grateful and rejoices wonderfully.",
            ),
        ],
    },
    "G065": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the Taronites praise letter and military/administrative alternatives against Gautier."],
        "notes": ["Checked against Gautier II, letter 65."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G070": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the praise-as-oikonomia argument and the final greetings from Theophylact's brothers/students against Gautier."],
        "notes": ["Checked against Gautier II, letter 70."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G071": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the description of Theophylact's earlier life as quiet/simple, not useless.",
            "Removed an unsupported shield image.",
            "Corrected the horse-control phrase to coaxing/soothing rather than shouting down.",
        ],
        "notes": [
            "Checked against Gautier II, letter 71.",
            "The letter combines the hare/frog fable, Homeric chariot imagery, and a Bulgarian-administration exhortation.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            ("inactive and useless", "quiet and simple"),
            ("throwing your shield behind you like a coward in the crowd", "turning your back like a coward in the crowd"),
            ("once you have shouted them down", "once you have coaxed them"),
        ],
    },
    "G072": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the mutual-prayer phrase so the prayers are allies against those causing grief.",
            "Corrected the closing thorn image from `those who fail` to afflictions/those causing grief.",
        ],
        "notes": [
            "Checked against Gautier II, letter 72.",
            "The letter invokes Moses' raised hands against Amalek and identifies the adversary as the apostate/tyrant of the world.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "to address one another and to invoke one another's prayers, as people call on allies when they are failing - we greet your holiness through this little letter of ours.",
                "to address one another and to invoke one another's prayers as allies against those who grieve us - we greet your holiness through this little letter of ours.",
            ),
            (
                "having yourself become entangled in the many thorns of those who fail, you need their removal;",
                "having yourself privately become caught in the many thorns of afflictions, you too need their removal;",
            ),
        ],
    },
    "G076": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_astrological_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected the Phoenix of Heliopolis image.",
            "Restored the Dog-star/Sirius heat image.",
            "Corrected `provocations and slanders` to the malefic astral appearances required by Gautier's note.",
        ],
        "notes": [
            "Checked against Gautier II, letter 76.",
            "Gautier flags `epiphauseis` as a hapax or corrupt reading in an astrological context; confidence remains B.",
        ],
        "unresolved": ["The exact sense of the astrological `epiphauseis` phrase remains uncertain."],
        "replacements": [
            ("that phoenix-sun", "the Phoenix of Heliopolis"),
            ("by otherwise concealing the night", "for me, condemned otherwise to night"),
            ("make the day longer for me for me, condemned otherwise to night", "make the day longer for me, condemned otherwise to night"),
            ("but when the sun has sprung up and left the lovely lake, we do not even see the dew.", "but when the sun has sprung up and left the lovely lake, at dawn we no longer see them at all."),
            ("You will certainly not plead your work through the nights.", "You will certainly not plead your work through the nights as an excuse."),
            (
                "You know our sicknesses, and especially the present ones, when the Lord has laid a burning heat upon us and melted away all life-giving moisture.",
                "You know our sicknesses, and especially the present ones, when the Dog-star, the terrible burner, has risen over us, laid a fierce heat upon us, and melted away all life-giving moisture.",
            ),
            ("since provocations and slanders will never leave us", "since malefic astral appearances will never leave us"),
        ],
    },
    "G080": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the self-condemnation, nature/law/gospel argument, and Galatians/Ephesians allusions against Gautier."],
        "notes": ["Checked against Gautier II, letter 80."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G083": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Restored the missing `salt` in the closing triad: salt, light, and leaven."],
        "notes": ["Checked against Gautier II, letter 83."],
        "unresolved": ["None material for the translation."],
        "replacements": [("as both light and leaven", "as salt, light, and leaven")],
    },
    "G084": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the refusal/shame logic in the opening Antilochus appeal."],
        "notes": [
            "Checked against Gautier II, letter 84.",
            "The two companion letters mentioned by Theophylact are lost, but this letter itself is complete.",
        ],
        "unresolved": ["None material for the surviving letter."],
        "replacements": [
            (
                "But this will not happen; therefore neither will what would follow it.",
                "But this will not happen; therefore neither will the refusal that would produce it.",
            ),
        ],
    },
    "G086": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the Bryennios praise letter, messenger notice, and Psalm 90 closing against Gautier."],
        "notes": ["Checked against Gautier II, letter 86."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G089": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_corrupt_word",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected the 1 Corinthians 11 allusion: many are weak/sick and a fair number sleep; this is not about canons.",
            "Corrected the final divine epithet to `indignant at wickedness`, while noting Gautier's conjecture.",
        ],
        "notes": [
            "Checked against Gautier II, letter 89.",
            "Gautier marks the final `wickedness` word as a proposed correction of a corrupt manuscript reading.",
        ],
        "unresolved": ["Final `poneriais` correction and the two Bulgarian opponents remain B-level uncertainties."],
        "replacements": [
            ("For this reason many among us are weak and sick, and the canons are asleep.", "For this reason many among us are weak and sick, and a fair number sleep."),
            ("the just God who is indignant at the heights", "the just God who is indignant at wickedness"),
        ],
    },
    "G090": {
        "confidence": "B",
        "status": "gautier_collated_clause_checked_with_localized_uncertainty",
        "condition": "gautier_collated_complete_with_localized_uncertainty",
        "changes": [
            "Corrected `lot` to the daimon/fortune language of the Greek.",
            "Capitalized `the Churches` where Gautier takes the phrase as the chorion Les Eglises.",
        ],
        "notes": [
            "Checked against Gautier II, letter 90.",
            "Gautier notes an obscure sentence and links `the Churches` to the chorion Les Eglises.",
        ],
        "unresolved": ["The `polyphoros daimon` sentence remains locally difficult."],
        "replacements": [
            ("We have been mixed with so prolific a lot", "We have been mixed with so trouble-bearing a daimon"),
            ("toward abandoning the churches", "toward abandoning the Churches"),
        ],
    },
    "G095": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Restored the Titus 3:5-based closing prayer; the first pass incorrectly made Theophylact's weakness an object of the oppressors."],
        "notes": [
            "Checked against Gautier II, letter 95.",
            "The last sentence alludes to Titus 3:5.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "May you yourself fare more easily than such things, so that those who afflict virtue may not prosper in everything. We have made our own weakness one of their objects, but because of your own goodness, may the outcome be better.",
                "But may you yourself be more lightly touched by such things, so that those who afflict virtue may not prosper in everything. May the Lord deliver our own weakness from them too, not because of any righteous deeds we have done, but because of his own goodness.",
            ),
        ],
    },
    "G099": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Lowercased and clarified `logos` where the Greek means discourse/reason/education rather than a direct Christological title."],
        "notes": ["Checked against Gautier II, letter 99."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            ("Great thanks to the Word", "Great thanks to logos"),
            ("for rational midwifery and nurture", "for midwifery and nurture in logos"),
            ("from the Word to shake off at the right moment", "from logos to discharge at the right moment"),
        ],
    },
    "G100": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the phrase about the enemies wasting away; the first pass turned it into an exhortation to prick them again."],
        "notes": [
            "Checked against Gautier II, letter 100.",
            "The superior Logos/eagle image is retained, while the following enemy phrase is translated literally.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "But do not neglect to prick these men once or twice more. Even if you hear the enemies of truth still blaspheming us",
                "But as for these men, let one or two of them waste away. And if you hear the enemies of truth still blaspheming us",
            ),
        ],
    },
    "G104": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the Attaliates/protonotarios recommendation against Gautier."],
        "notes": ["Checked against Gautier II, letter 104."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G105": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the symbolic fish gift to Bryennios against Gautier and retained the Logos/Leviathan/salt structure."],
        "notes": ["Checked against Gautier II, letter 105."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G106": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Restored `day after day` and standardized `praktor` in the anthill-of-misfortunes image."],
        "notes": ["Checked against Gautier II, letter 106."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "heaped up by our sins as they sit and use the tax official as their servant.",
                "heaped up day after day by our sins, which use the praktor as their servant.",
            ),
        ],
    },
    "G108": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Checked the Prespa synod letter and cicada/starvation joke against Gautier."],
        "notes": ["Checked against Gautier II, letter 108."],
        "unresolved": ["None material for the translation."],
        "replacements": [],
    },
    "G112": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the parable-of-the-sower imagery: the bird is a thought of disdain, not a premature winged conceit."],
        "notes": [
            "Checked against Gautier II, letter 112.",
            "The request is for Galenic/Hippocratic theoretical works, especially the Hippocrates/Plato doctrines treatise.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            ("no winged and premature conceit", "no bird - that is, no thought of disdain"),
            ("the cares of technical work as an objection to the books", "the cares of technical work as excuses against lending the books"),
        ],
    },
    "G113": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Corrected the opening appeal: Theophylact asks the bishop to help him better, not merely understand him.",
            "Clarified the Achrida wine phrase.",
        ],
        "notes": [
            "Checked against Gautier II, letter 113.",
            "The letter concerns Demetrios' illness at the chorion called the Churches.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "Understand me in a better way, all-holy brother and master, and do not let the chaff concern me when I possess the wheat.",
                "Come to my aid more effectively, all-holy brother and master, and the chaff will not concern me while I possess the wheat.",
            ),
            ("my brother, whom I still possess as sparks", "my brother, whom I still possess as the last spark"),
            ("the light, thin wine there", "the wine there, which bears little water and is very light"),
            ("very light and of other healthier foods", "very light, and of other healthier foods"),
        ],
    },
    "G118": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": [
            "Standardized Vardarion spelling.",
            "Restored `harmostes` and corrected `under-voices` to encouraging acclamations.",
        ],
        "notes": ["Checked against Gautier II, letter 118."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            ("governor over the affairs of Bardarion", "harmostes over the affairs of Vardarion"),
            ("possess an estate in Bardarion", "possess an estate in Vardarion"),
            ("we are accustomed to give wings with our under-voices even to those who run well", "we are accustomed to give wings with encouraging acclamations even to those who run well"),
        ],
    },
    "G119": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Tightened the Theotokos title in line with Gautier's Greek."],
        "notes": ["Checked against Gautier II, letter 119."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            ("our Lady, the Mother of God and Theotokos", "our Lady and Mother, the Theotokos"),
        ],
    },
    "G123": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the closing chain metaphor: the point is not to loosen the golden chain, not not to depart."],
        "notes": ["Checked against Gautier II, letter 123."],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "To exhort you not to depart would belong neither to one who has perceived your magnanimous nature nor to one who nourishes rich and noble hopes in you.",
                "To exhort you not to loosen it would belong neither to one who has perceived your magnanimous nature nor to one who nourishes rich and noble hopes in you.",
            ),
        ],
    },
    "G129": {
        "confidence": "A",
        "status": "gautier_collated_clause_checked_complete",
        "condition": "gautier_collated_complete",
        "changes": ["Corrected the beggar joke: he asks for crusts, not swords or cauldrons."],
        "notes": [
            "Checked against Gautier II, letter 129.",
            "The line echoes Odyssey 17.222.",
        ],
        "unresolved": ["None material for the translation."],
        "replacements": [
            (
                "will regard your presence as that of some poor man who goes about begging, asking not for breads or pots, and if he receives some small thing, content with what has been received.",
                "will regard your presence as that of some poor man going about begging for crusts, not for swords or cauldrons, and, if he receives even some small thing, content with what he has received.",
            ),
        ],
    },
}


def bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def update_file(gid: str, update: dict) -> None:
    path = LETTERS / gid / "translation_v2.md"
    text = path.read_text(encoding="utf-8")

    for old, new in update["replacements"]:
        text = replace_required(text, old, new, gid)

    text = set_line(text, "Second-pass status: ", update["status"])
    text = set_line(text, "Confidence category: ", update["confidence"])
    text = set_line(text, "- Source condition: ", update["condition"])
    text = replace_section(text, "Consequential Changes From First Pass", bullet_lines(update["changes"]))
    text = replace_section(text, "Source And Revision Notes", bullet_lines(update["notes"]))
    text = replace_section(text, "Unresolved Issues", bullet_lines(update["unresolved"]))

    trail = f"- {TODAY}: Extended Gautier clause audit completed; confidence set to {update['confidence']}."
    if trail not in text:
        text = text.rstrip() + "\n" + trail + "\n"

    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for gid, update in sorted(UPDATES.items()):
        update_file(gid, update)
    print(f"Updated {len(UPDATES)} extended Gautier audits.")


if __name__ == "__main__":
    main()
