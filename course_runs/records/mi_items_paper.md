# mi_items_paper

_Items for the paper experiments P1 (ko insertion), P2 (role swap) and P6 (marker control matched in kind). Rerun under the same tag: the first run is superseded by the fixes after the independent review (particle skips, default-form test, object features, secondary control ctls)._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 00:03 |
| script | `mi_items_paper.py` (sha256 `ff427bbde8239655`) |
| host | gnode (Linux) |
| duration | 0.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"out_dir": null, "record_tag": "mi_items_paper"}` |
| command | `scripts/mi_items_paper.py` |


- **fresh agreement orders read**: 2,179 of 5,265
- **clauses whose subject and object features were read from the tree**: 294

| P2 swap | count |
|---|---|
| fresh orders read | 2179 |
| kept | 2132 |
| skipped: subject phrase not contiguous | 43 |
| skipped: object phrase not contiguous | 4 |
| equal-length phrases | 418 |


| P1 ko | count |
|---|---|
| fresh orders read | 2179 |
| entering | 956 |
| skipped: subject not masculine singular | 1205 |
| skipped: object phrase ends in a listed particle or postposition | 12 |
| skipped: foil agreeing words not all default forms | 1 |
| skipped: object phrase is followed by a listed particle or postposition | 2 |
| skipped: object phrase not contiguous | 3 |
| clauses entering | 130 |
| distinct object head words entering | 87 |
| documents entering | 118 |


| P1: entering orders by object number | orders | documents |
|---|---|---|
| feminine singular | 728 | 85 |
| masculine singular | 0 | 0 |
| plural | 228 | 35 |
| other | 0 | 0 |


| P2: swapcorrect_default (rows) by origcorrect_default (columns) | origcorrect_default False | origcorrect_default True |
|---|---|---|
| swapcorrect_default False | 273 | 924 |
| swapcorrect_default True | 935 | 0 |


| swap: order class | orders | documents |
|---|---|---|
| SOV | 1142 | 233 |
| OSV | 990 | 146 |
| reference orders | 285 | 235 |


| ko: order class | orders | documents |
|---|---|---|
| SOV | 510 | 118 |
| OSV | 446 | 74 |
| reference orders | 130 | 118 |


### Examples (orig/none, then the edited version)

- swap | before: correct: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखी । || foil: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखा । || obj 9|10 subj 0|1 ne 2 agree 11
- swap | after:  correct: एक शर्त ने चित्‍तौड़ पर आक्रमण करने के बाद अलाउद्दीन खिलजी रखा । || foil: एक शर्त ने चित्‍तौड़ पर आक्रमण करने के बाद अलाउद्दीन खिलजी रखी । || obj 9|10 subj 0|1 ne 2 agree 11
- swap | before: correct: पड़ोस के राज्य में गन्ने का न्यूनतम मूल्य १३५ रुपये क्विंटल सरकार ने घोषित कर रखा है , जबकि उत्तर प्रदेश में यह अधिकतम १२० रुपये क्विंटल है । || foil: पड़ोस के राज्य में गन्ने का न्यूनतम मूल्य १३५ रुपये क्विंटल सरकार ने घोषित कर रखी है , जबकि उत्तर प्रदेश में यह अधिकतम १२० रुपये क्विंटल है । || obj 4|5|6|7|8|9|10 subj 11 ne 12 agree 15
- swap | after:  correct: पड़ोस के राज्य में सरकार गन्ने का न्यूनतम मूल्य १३५ रुपये क्विंटल ने घोषित कर रखी है , जबकि उत्तर प्रदेश में यह अधिकतम १२० रुपये क्विंटल है । || foil: पड़ोस के राज्य में सरकार गन्ने का न्यूनतम मूल्य १३५ रुपये क्विंटल ने घोषित कर रखा है , जबकि उत्तर प्रदेश में यह अधिकतम १२० रुपये क्विंटल है । || obj 4 subj 5|6|7|8|9|10|11 ne 12 agree 15
- swap | before: correct: एक और सनसनीखेज जानकारी आतंकी ट्रेनिंग लेने के लिए वजा ने शुरुआती दौर में ही नियंत्रण रेखा के पार जाने वाले कश्मीरियों में से दी है । || foil: एक और सनसनीखेज जानकारी आतंकी ट्रेनिंग लेने के लिए वजा ने शुरुआती दौर में ही नियंत्रण रेखा के पार जाने वाले कश्मीरियों में से दिया है । || obj 0|1|2|3 subj 9 ne 10 agree 24
- swap | after:  correct: वजा आतंकी ट्रेनिंग लेने के लिए एक और सनसनीखेज जानकारी ने शुरुआती दौर में ही नियंत्रण रेखा के पार जाने वाले कश्मीरियों में से दिया है । || foil: वजा आतंकी ट्रेनिंग लेने के लिए एक और सनसनीखेज जानकारी ने शुरुआती दौर में ही नियंत्रण रेखा के पार जाने वाले कश्मीरियों में से दी है । || obj 0 subj 6|7|8|9 ne 10 agree 24
- ko feminine singular | before: correct: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखी । || foil: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखा । || obj 9|10 subj 0|1 ne 2 agree 11
- ko feminine singular | after:  correct: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त को रखा । || foil: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त को रखी । || obj 9|10 subj 0|1 ne 2 agree 12
- ko feminine singular | before: correct: रानी पद्मिनी ने तालाब के सामने अपना घूँघट खोला , वह छवि तालाब के सामने स्थित दुमंजिला बरामदे में लगाए गए आईने में अलाउद्दीन ने देखी और वह अपनी सेनाओं समेत वापस लौट गया । || foil: रानी पद्मिनी ने तालाब के सामने अपना घूँघट खोला , वह छवि तालाब के सामने स्थित दुमंजिला बरामदे में लगाए गए आईने में अलाउद्दीन ने देखा और वह अपनी सेनाओं समेत वापस लौट गया । || obj 10|11 subj 23 ne 24 agree 25
- ko feminine singular | after:  correct: रानी पद्मिनी ने तालाब के सामने अपना घूँघट खोला , वह छवि को तालाब के सामने स्थित दुमंजिला बरामदे में लगाए गए आईने में अलाउद्दीन ने देखा और वह अपनी सेनाओं समेत वापस लौट गया । || foil: रानी पद्मिनी ने तालाब के सामने अपना घूँघट खोला , वह छवि को तालाब के सामने स्थित दुमंजिला बरामदे में लगाए गए आईने में अलाउद्दीन ने देखी और वह अपनी सेनाओं समेत वापस लौट गया । || obj 10|11 subj 24 ne 25 agree 26
- ko feminine singular | before: correct: गुरू जी ने ही स्वतंत्रता आंदोलन में व्यक्तिगत तौर पर शामिल होने की आज्ञा स्वयंसेवकों को दी थी । || foil: गुरू जी ने ही स्वतंत्रता आंदोलन में व्यक्तिगत तौर पर शामिल होने की आज्ञा स्वयंसेवकों को दिया था । || obj 4|5|6|7|8|9|10|11|12|13 subj 0|1|3 ne 2 agree 16|17
- ko feminine singular | after:  correct: गुरू जी ने ही स्वतंत्रता आंदोलन में व्यक्तिगत तौर पर शामिल होने की आज्ञा को स्वयंसेवकों को दिया था । || foil: गुरू जी ने ही स्वतंत्रता आंदोलन में व्यक्तिगत तौर पर शामिल होने की आज्ञा को स्वयंसेवकों को दी थी । || obj 4|5|6|7|8|9|10|11|12|13 subj 0|1|3 ne 2 agree 17|18
- ko plural | before: correct: सुनीत ने दो तस्वीरें पेश कीं । || foil: सुनीत ने दो तस्वीरें पेश किया । || obj 2|3 subj 0 ne 1 agree 5
- ko plural | after:  correct: सुनीत ने दो तस्वीरें को पेश किया । || foil: सुनीत ने दो तस्वीरें को पेश कीं । || obj 2|3 subj 0 ne 1 agree 6
- ko plural | before: correct: दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने इस दिशा में कुछ निष्कर्ष अध्ययन करके निकाले । || foil: दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने इस दिशा में कुछ निष्कर्ष अध्ययन करके निकाला । || obj 12|13 subj 0|1|2|3|4|5|6|7 ne 8 agree 16
- ko plural | after:  correct: दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने इस दिशा में कुछ निष्कर्ष को अध्ययन करके निकाला । || foil: दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने इस दिशा में कुछ निष्कर्ष को अध्ययन करके निकाले । || obj 12|13 subj 0|1|2|3|4|5|6|7 ne 8 agree 17
- ko plural | before: correct: इस दिशा में अध्ययन करके दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने कुछ निष्कर्ष निकाले । || foil: इस दिशा में अध्ययन करके दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने कुछ निष्कर्ष निकाला । || obj 14|15 subj 5|6|7|8|9|10|11|12 ne 13 agree 16
- ko plural | after:  correct: इस दिशा में अध्ययन करके दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने कुछ निष्कर्ष को निकाला । || foil: इस दिशा में अध्ययन करके दिल्ली विश्वविद्यालय के कानून विभाग के एक प्रोफेसर ने कुछ निष्कर्ष को निकाले । || obj 14|15 subj 5|6|7|8|9|10|11|12 ne 13 agree 17
- bhi | before: correct: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखी । || foil: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखा । || obj 9|10 subj 0|1 ne 2 agree 11
- bhi | after:  correct: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त भी रखी । || foil: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त भी रखा । || obj 9|10 subj 0|1 ne 2 agree 12
- bhi | before: correct: आज शनिवार को बनारस में अटकने के बाद रफ्तार मानसून ने फिर पकड़ ली । || foil: आज शनिवार को बनारस में अटकने के बाद रफ्तार मानसून ने फिर पकड़ लिया । || obj 8 subj 9 ne 10 agree 13
- bhi | after:  correct: आज शनिवार को बनारस में अटकने के बाद रफ्तार भी मानसून ने फिर पकड़ ली । || foil: आज शनिवार को बनारस में अटकने के बाद रफ्तार भी मानसून ने फिर पकड़ लिया । || obj 8 subj 10 ne 11 agree 14
- bhi | before: correct: इसी बीच ट्रेन की चेन दूसरे जवान ने खींच दी . || foil: इसी बीच ट्रेन की चेन दूसरे जवान ने खींच दिया . || obj 2|3|4 subj 5|6 ne 7 agree 9
- bhi | after:  correct: इसी बीच ट्रेन की चेन भी दूसरे जवान ने खींच दी . || foil: इसी बीच ट्रेन की चेन भी दूसरे जवान ने खींच दिया . || obj 2|3|4 subj 6|7 ne 8 agree 10
- skipped, object ends in or is followed by a particle | before: correct: इसके पास ही पिट्जर टेलीस्कोप ने कुछ धूल के कणों के साक्ष्य भी पाए गए हैं जो बर्फ़ , मिथेनॉल और कार्बन डाइऑक्साइड की परत से ढंके हैं . || foil: इसके पास ही पिट्जर टेलीस्कोप ने कुछ धूल के कणों के साक्ष्य भी पाया गया है जो बर्फ़ , मिथेनॉल और कार्बन डाइऑक्साइड की परत से ढंके हैं . || obj 6|7|8|9|10|11|12 subj 3|4 ne 5 agree 13|14|15
- skipped, object ends in or is followed by a particle | before: correct: अमीन ने कहा कि जीसीए ने हर गैलरी के सामने पीने के पानी , नाश्ते और भोजन के लिए पर्याप्त व्यवस्था की है । || foil: अमीन ने कहा कि जीसीए ने हर गैलरी के सामने पीने के पानी , नाश्ते और भोजन के लिए पर्याप्त व्यवस्था किया है । || obj 19|20 subj 4 ne 5 agree 21
- skipped, object ends in or is followed by a particle | before: correct: जेल से मुक्ति की राह देख रहे शंकराचार्य जयेंद्र सरस्वती को बुधवार को तगड़ा झटका लगा जब मद्रास हाईकोर्ट ने उनकी दूसरी जमानत अर्जी भी खारिज कर दी । || foil: जेल से मुक्ति की राह देख रहे शंकराचार्य जयेंद्र सरस्वती को बुधवार को तगड़ा झटका लगा जब मद्रास हाईकोर्ट ने उनकी दूसरी जमानत अर्जी भी खारिज कर दिया । || obj 20|21|22|23|24 subj 17|18 ne 19 agree 27
- skipped, foil not a default form | before: correct: उन्होंने यह भी बताया कि प्रारंभिक जांच में यह बात सामने आई है कि शहाबुद्दीन खुद एलएलबी की परीक्षा देने नहीं आए थे , बल्कि एडमिट कार्ड , अटेनडेंस शीट व अन्य फर्जी दस्तावेजों के आधार पर उनके बदले किसी और ने उनकी कॉपी लिखी । || foil: उन्होंने यह भी बताया कि प्रारंभिक जांच में यह बात सामने आई है कि शहाबुद्दीन खुद एलएलबी की परीक्षा देने नहीं आए थे , बल्कि एडमिट कार्ड , अटेनडेंस शीट व अन्य फर्जी दस्तावेजों के आधार पर उनके बदले किसी और ने उनकी कॉपी लिखे । || obj 42|43 subj 39|40 ne 41 agree 44

| P6 kind | count |
|---|---|
| fresh pairs with n_psp >= 1 | 420 |
| entering primary test (kind_ok) | 131 |
| entering secondary test (ctls_ok) | 17 |
| entering both | 15 |
| documents entering the primary test | 121 |
| documents entering the secondary test | 17 |
| markers deleted per kind_ok pair (mean) | 1.6107 |


## P6: word distance of the deleted words to the nearest moved head word, and genitive share


| set of deleted words | words | mean distance | median distance | genitive (का, की, के) | other |
|---|---|---|---|---|---|
| markers (kind_ok pairs) | 211 | 1.13 | 1 | 13 of 211 (6%) | 198 of 211 (94%) |
| ctlk | 211 | 9.68 | 8 | 97 of 211 (46%) | 114 of 211 (54%) |
| markers (ctls_ok pairs) | 19 | 1.11 | 1 | 1 of 19 (5%) | 18 of 19 (95%) |
| ctls | 19 | 10.1 | 7 | 1 of 19 (5%) | 18 of 19 (95%) |


| string | markers (kind_ok pairs) | ctlk | markers (ctls_ok pairs) | ctls |
|---|---|---|---|---|
| में | 62 | 29 | 9 | 9 |
| ने | 43 | 13 | 1 | 1 |
| को | 27 | 24 | 1 | 1 |
| से | 23 | 29 | 1 | 1 |
| पर | 17 | 18 | 3 | 3 |
| के | 10 | 49 | 1 | 1 |
| तक | 5 | 1 | 1 | 1 |
| पहले | 4 | 0 | 0 | 0 |
| लिए | 4 | 0 | 1 | 1 |
| की | 3 | 36 | 0 | 0 |
| हवाले | 2 | 0 | 0 | 0 |
| बारे | 2 | 0 | 0 | 0 |
| मुताबिक | 2 | 0 | 0 | 0 |
| ओर | 1 | 0 | 0 | 0 |
| ख़िलाफ़ | 1 | 0 | 0 | 0 |
| बाद | 1 | 0 | 0 | 0 |
| वजह | 1 | 0 | 0 | 0 |
| साथ | 1 | 0 | 0 | 0 |
| पास | 1 | 0 | 0 | 0 |
| बाबत | 1 | 0 | 0 | 0 |
| का | 0 | 12 | 0 | 0 |
| द्वारा | 0 | 0 | 1 | 1 |


| per pair: mean of the pair's mean distances | dist_psp | dist_ctlk | dist_ctls |
|---|---|---|---|
| kind_ok pairs | 1.09 | 8.88 | - |
| ctls_ok pairs | 1.09 | - | 10.3 |


### Examples (reference text, then the same pair with the listed words deleted)

- ctlk | before: ref अपनी वापसी को उन्होंने तकनीकी मामला बताया और उसे राजनीति शुद्धता से जोड़ दिया । || var तकनीकी मामला उन्होंने अपनी वापसी को बताया और उसे राजनीति शुद्धता से जोड़ दिया ।
- ctlk | after (dropped variant words 11): ref अपनी वापसी को उन्होंने तकनीकी मामला बताया और उसे राजनीति शुद्धता जोड़ दिया । || var तकनीकी मामला उन्होंने अपनी वापसी को बताया और उसे राजनीति शुद्धता जोड़ दिया ।
- ctlk | before: ref यहां एक सेमीनार में अय्यर ने स्वीकार किया कि पेट्रोलियम मंत्रालय के अधिकारियों और उनके बीच छत्तीस का आंकड़ा था । || var अय्यर ने यहां एक सेमीनार में स्वीकार किया कि पेट्रोलियम मंत्रालय के अधिकारियों और उनके बीच छत्तीस का आंकड़ा था ।
- ctlk | after (dropped variant words 11|17): ref यहां एक सेमीनार में अय्यर ने स्वीकार किया कि पेट्रोलियम मंत्रालय अधिकारियों और उनके बीच छत्तीस आंकड़ा था । || var अय्यर ने यहां एक सेमीनार में स्वीकार किया कि पेट्रोलियम मंत्रालय अधिकारियों और उनके बीच छत्तीस आंकड़ा था ।
- ctlk | before: ref इस बारे में माकपा पोलित ब्यूरो की ओर से जारी बयान में कहा गया है कि राज्यपाल के अधिकार के प्रावधान के मुताबिक राज्यपाल को अपने विचारों से राज्य सरकार को अवगत कराना चाहिए और अपनी सलाह देनी चाहिए . || var माकपा पोलित ब्यूरो की ओर से जारी बयान में इस बारे में कहा गया है कि राज्यपाल के अधिकार के प्रावधान के मुताबिक राज्यपाल को अपने विचारों से राज्य सरकार को अवगत कराना चाहिए और अपनी सलाह देनी चाहिए .
- ctlk | after (dropped variant words 24|27|30): ref इस बारे में माकपा पोलित ब्यूरो की ओर से जारी बयान में कहा गया है कि राज्यपाल के अधिकार के प्रावधान के मुताबिक राज्यपाल अपने विचारों राज्य सरकार अवगत कराना चाहिए और अपनी सलाह देनी चाहिए . || var माकपा पोलित ब्यूरो की ओर से जारी बयान में इस बारे में कहा गया है कि राज्यपाल के अधिकार के प्रावधान के मुताबिक राज्यपाल अपने विचारों राज्य सरकार अवगत कराना चाहिए और अपनी सलाह देनी चाहिए .
- ctls | before: ref वित्त निगम द्वारा ११० करोड़ व इरकक द्वारा १८.७५ करोड़ का चेक सौंपा गया । || var वित्त निगम द्वारा ११० करोड़ व १८.७५ करोड़ का चेक इरकक द्वारा सौंपा गया ।
- ctls | markers (variant words) [11]: ['द्वारा']; controls [2]: ['द्वारा']
- ctls | after: ref वित्त निगम ११० करोड़ व इरकक द्वारा १८.७५ करोड़ का चेक सौंपा गया । || var वित्त निगम ११० करोड़ व १८.७५ करोड़ का चेक इरकक द्वारा सौंपा गया ।

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `agreement_swap.csv` | 3,109,315 | `cceb6ef4197090ea` | P2: fresh orders, orig and subject/object-swapped versions |
| `agreement_ko.csv` | 1,999,506 | `833e7e0887a0e471` | P1: fresh orders with a masculine singular subject, none / ko / bhi versions |
| `wordorder_kind.csv` | 178,416 | `8e5781cc1714e65e` | P6: fresh pairs with moved markers, the controls matched in kind (ctlk) and in kind and place (ctls) |
