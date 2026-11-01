"""Vietnamese captions, hooks, cards, and motion labels keep every letter without changing other languages."""
from pathlib import Path
import sys
import tempfile
import unittest

HELPERS = Path(__file__).resolve().parents[2] / 'skills/nhipdung/engine/helpers'
sys.path.insert(0, str(HELPERS))
import assemble_cut  # noqa: E402
import captions  # noqa: E402
import spoken_numbers as vl  # noqa: E402
import suggest_visuals as sv  # noqa: E402
import text_render as tr  # noqa: E402
import transcribe  # noqa: E402
from visuals import engine as E  # noqa: E402

VIETNAMESE = 'Xin chào Việt Nam, cảm ơn các bạn đã xem video này'
PORTUGUESE = 'Obrigado por assistir, até a próxima semana'


class FontChoiceTests(unittest.TestCase):
    def test_letters_a_font_lacks_switch_to_its_fallback_only_when_needed(self):
        for key, fallback in (('text_bold', 'text_bold_extended'), ('text_semibold', 'text_semibold_extended'),
                              ('marker', 'marker_extended'), ('hand', 'hand_extended')):
            with self.subTest(key=key):
                self.assertEqual(tr.font_for_texts(key, [VIETNAMESE]), fallback)
                self.assertEqual(tr.font_for_texts(key, [PORTUGUESE]), key)
                self.assertEqual(tr.sanitize_text(VIETNAMESE, fallback), (VIETNAMESE, []))
        # fonts that already draw Vietnamese keep their own typeface
        for key in ('sans_black', 'sans_extrabold', 'display_condensed'):
            self.assertEqual(tr.font_for_texts(key, [VIETNAMESE]), key)

    def test_emoji_alone_never_switches_the_typeface(self):
        self.assertEqual(tr.font_for_texts('text_bold', ['Obrigado 🎬 →']), 'text_bold')

    def test_one_vietnamese_name_keeps_the_whole_track_on_one_font(self):
        words = ['Hoje', 'falamos', 'com', 'Nguyễn', 'sobre', 'vendas']
        font = tr.caption_font('clean_caption', words)
        self.assertEqual(font, 'text_bold_extended')
        self.assertEqual(tr.display_words(words, 'clean_caption', font), words)
        # Figtree has no ễ of its own: shaping rebuilds it from e and a tilde and drops the circumflex (ẽ)
        self.assertFalse(tr._has_own_glyph('text_bold', 'ễ'))
        self.assertTrue(tr._has_own_glyph('text_bold_extended', 'ễ'))

    def test_text_issues_no_longer_report_vietnamese_letters(self):
        self.assertEqual(tr.text_issues('caption', VIETNAMESE, 'clean_caption'), [])
        self.assertEqual(tr.text_issues('hook', 'Đừng bỏ lỡ *bí quyết* này', 'marker'), [])
        self.assertEqual(tr.text_issues('cta_sub', 'Ưu đãi chỉ trong hôm nay'), [])
        self.assertEqual(tr.text_issues('disclaimer', 'Kết quả có thể khác nhau tùy từng người'), [])

    def test_hook_layout_keeps_every_vietnamese_word(self):
        fit = tr.hook_fit('Đừng bỏ lỡ *bí quyết* này', 'marker')
        self.assertEqual(' '.join(fit['lines']), 'ĐỪNG BỎ LỠ BÍ QUYẾT NÀY')

    def test_caption_cues_measure_and_display_with_the_track_font(self):
        words = [{'text': w, 'start': i * 0.4, 'end': i * 0.4 + 0.35, 'seg': 0}
                 for i, w in enumerate('Cảm ơn các bạn đã xem video này'.split())]
        cues = captions.build_cues(words, 'clean_caption', 8, (1080, 1920), [(0.0, 4.0, 0.0)])
        self.assertEqual(' '.join(c['text'] for c in cues), 'Cảm ơn các bạn đã xem video này')

    def test_caption_track_renders_vietnamese_without_removing_letters(self):
        cues = {'cues': [{'start': 0.0, 'end': 1.2, 'text': 'Cảm ơn các bạn',
                          'words': [{'text': w, 'start': i * 0.3, 'end': i * 0.3 + 0.28} for i, w in enumerate(['Cảm', 'ơn', 'các', 'bạn'])]}]}
        with tempfile.TemporaryDirectory() as temp:
            states = tr.render_caption_track(cues, 'clean_caption', '#FFC400', temp, (540, 960), 30)
            self.assertTrue(states and all(s['bbox'] for s in states))
        above, below = tr.caption_extent(cues, 'clean_caption', (540, 960))
        self.assertGreater(above, 0)
        self.assertGreater(below, 0)

    def test_stacked_vietnamese_marks_count_as_reaching_above(self):
        for ch in 'ẤẦẨẪẬẮẰẲẴẾỀỂỄỐỒỔỖỚỜỞỠỨỪỬỮ':
            self.assertIn(ch, tr._REACH_ABOVE)
        for ch in 'ẤẦẨẪẮẰẲẴẾỀỂỄỐỒỔỖ':
            self.assertIn(ch, tr._REACH_STACKED)
        for ch in 'ạậặẹệịọộợụựỵ':
            self.assertIn(ch, tr._REACH_BELOW)


class MotionItemTests(unittest.TestCase):
    def test_item_theme_swaps_only_fonts_that_lack_the_labels(self):
        theme = E.make_theme(E.DEFAULT_ACCENT, 'dark')
        swapped = dict(E.text_fonts(theme, E.param_texts({'title': 'Doanh thu', 'items': [{'label': 'Tháng một'}]})).fonts)
        self.assertEqual(swapped.get('text_bold'), 'text_bold_extended')
        self.assertEqual(swapped.get('text_semibold'), 'text_semibold_extended')
        self.assertNotIn('sans_black', swapped)
        self.assertIs(E.text_fonts(theme, ['Receita mensal']), theme)

    def test_paper_theme_keeps_its_own_swaps_and_extends_the_handwriting(self):
        paper = next(iter(E.PAPER))
        theme = E.make_theme(E.DEFAULT_ACCENT, paper)
        swapped = dict(E.text_fonts(theme, ['Chúc mừng năm mới']).fonts)
        self.assertEqual(swapped['marker'], 'hand_extended')
        self.assertEqual(swapped['text_bold'], 'sans_extrabold')
        with E.theme_fonts(E.text_fonts(theme, ['Chúc mừng năm mới'])):
            self.assertEqual(E.clean_text('Chúc mừng năm mới', 'marker'), 'Chúc mừng năm mới')


class LexiconTests(unittest.TestCase):
    def test_filler_only_blocks_match_as_said(self):
        for word in ('ờ', 'ừm', 'à', 'ơ', 'thì', 'kiểu', 'Ờ,', 'então', 'né', 'tá', 'aí', 'hã'):
            self.assertIn(assemble_cut.spoken_value(word), assemble_cut.HESITATION, word)
        for word in ('không', 'được', 'vâng', 'dạ', 'bạn', 'triệu', 'vendas', 'o', 'a', 'um', 'há'):
            self.assertNotIn(assemble_cut.spoken_value(word), assemble_cut.HESITATION, word)

    def test_vietnamese_subtitle_credit_is_dropped_only_over_silence(self):
        phrase = 'Hãy subscribe cho kênh Ghiền Mì Gõ để không bỏ lỡ những video hấp dẫn'.split()
        words = [{'text': w, 'start': i * 0.2, 'end': i * 0.2 + 0.18, 'seg': 0} for i, w in enumerate(phrase)]
        kept, dropped = transcribe.known_phrase_guard(words, [[0.0, 4.0]])
        self.assertEqual((kept, dropped), ([], len(phrase)))
        kept, dropped = transcribe.known_phrase_guard(words, [])
        self.assertEqual(dropped, 0)

    def test_vietnamese_function_words_lean_on_the_next_word(self):
        for word in ('các', 'của', 'và', 'Những', 'để,'):
            self.assertTrue(tr.is_weak_word(word), word)
        for word in ('bạn', 'video', 'Việt'):
            self.assertFalse(tr.is_weak_word(word), word)
        self.assertTrue({vl.normal_value(w) for w in ('của', 'những', 'để', 'đó')} <= sv.FUNCTION_WORDS)


class VietnameseNumberTests(unittest.TestCase):
    NUMBERS = [('hai triệu rưỡi', 2_500_000), ('năm trăm nghìn', 500_000), ('một trăm linh năm', 105),
               ('hai mươi lăm', 25), ('mười lăm', 15), ('hai mươi tư', 24), ('ba mươi', 30), ('một triệu hai', 1_200_000),
               ('ba trăm năm mươi nghìn', 350_000), ('hai tỷ năm trăm triệu', 2_500_000_000), ('2,5 triệu', 2_500_000),
               ('500k', 500_000), ('5 củ', 5_000_000), ('nửa triệu', 500_000), ('một trăm hai', 120), ('trăm rưỡi', 150),
               ('hai nghìn không trăm linh năm', 2005), ('một triệu hai trăm nghìn', 1_200_000), ('Hai Triệu', 2_000_000)]

    def test_spoken_vietnamese_numbers(self):
        for spoken, value in self.NUMBERS:
            with self.subTest(spoken=spoken):
                self.assertEqual(vl.parse_number(spoken), value)

    def test_tone_marks_keep_numerals_apart_from_other_words(self):
        for phrase in ('mười năm', 'hai nghìn năm', 'sau ngày', 'Việt Nam'):
            with self.subTest(phrase=phrase):
                self.assertIsNone(vl.parse_number(phrase))
        self.assertEqual(vl.normal_value('sáu sau năm nam đô đó'), 'vi_sau sau vi_nam nam vi_do đo')

    def test_vietnamese_money_with_its_currency(self):
        cases = [('Giá chỉ còn 199.000đ thôi', '199.000đ', 199_000, '₫'), ('khóa học 500 nghìn đồng', None, 500_000, '₫'),
                 ('chỉ 50 đô', None, 50, '$'), ('199.000 ₫', None, 199_000, '₫')]
        for sentence, span, value, prefix in cases:
            with self.subTest(sentence=sentence):
                text = vl.normal_value(sentence)
                [money] = vl.find_money(text)
                self.assertEqual(money.value, value)
                self.assertFalse(money.bare)
                self.assertEqual(vl.currency_prefix(text[money.start:money.end]), prefix)
                if span:
                    self.assertEqual(text[money.start:money.end], span)

    def test_words_that_only_look_like_money_are_not_money(self):
        for sentence in ('mua hai đồng hồ', 'tôi không đồng ý', 'năm đó tôi ở Việt Nam', 'đồ cũ', 'hàng triệu người xem'):
            with self.subTest(sentence=sentence):
                self.assertEqual(vl.find_money(vl.normal_value(sentence)), [])

    def test_attached_scales_are_read_in_every_language(self):
        self.assertEqual(vl.parse_money('500k'), 500_000)
        self.assertEqual(vl.parse_money('10mil'), 10_000)


class VietnameseSuggestionTests(unittest.TestCase):
    @staticmethod
    def sentence(text):
        return sv.Sentence([sv.Word(text=w, normal_value=vl.normal_value(w), start=i * 0.4, end=i * 0.4 + 0.35)
                            for i, w in enumerate(text.split())])

    def test_prices_gains_counts_and_percentages(self):
        price = sv.find_price([self.sentence('Khóa học này giá chỉ còn 199 nghìn đồng thôi các bạn')])
        self.assertEqual([(c.template, c.params['price'], c.params['prefix']) for c in price], [('price_tag', 199_000, '₫')])
        old_new = sv.find_price([self.sentence('Từ 500 nghìn giảm còn 199 nghìn')])
        self.assertEqual((old_new[0].params['price'], old_new[0].params['old_price']), (199_000, 500_000))
        found = sv.find_numbers([self.sentence(t) for t in ('Tháng trước mình kiếm được hai triệu rưỡi mỗi tháng',
                                                               'Hơn 500 học viên đã hoàn thành khóa học',
                                                               'Tỷ lệ chốt đơn tăng 30 phần trăm')])
        self.assertEqual([(c.params['value'], c.params.get('suffix'), c.params.get('prefix')) for c in found],
                         [(2_500_000, None, ''), (500, 'học viên', '+'), (30, '%', None)])

    def test_no_suggestion_from_lookalike_words(self):
        sentence = self.sentence('Mua hai đồng hồ và không đồng ý với giá cũ')
        self.assertEqual(sv.find_price([sentence]) + sv.find_numbers([sentence]), [])


class ReviewRegressionTests(unittest.TestCase):
    """Defects found by the independent review of the first Vietnamese change."""

    @staticmethod
    def sentence(text):
        return sv.Sentence([sv.Word(text=w, normal_value=vl.normal_value(w), start=i * 0.4, end=i * 0.4 + 0.35)
                            for i, w in enumerate(text.split())])

    def counters(self, text):
        return [(c.params.get('value'), c.params.get('suffix'), c.params.get('prefix')) for c in sv.find_numbers([self.sentence(text)])]

    def test_digits_with_a_vietnamese_scale_and_unit_do_not_crash(self):
        self.assertEqual(self.counters('Kênh của mình có 2 triệu người theo dõi rồi'), [(2_000_000, 'người theo dõi', None)])
        self.assertEqual(self.counters('Hơn 500 nghìn học viên'), [(500_000, 'học viên', '+')])
        self.assertEqual(self.counters('3 tr lượt xem'), [(3_000_000, 'lượt xem', None)])

    def test_compounds_and_toneless_lookalikes_are_not_money_or_units(self):
        for text in ('Việt Nam có 2 đô thị đặc biệt', 'hơn 1 triệu đồng bào cả nước', 'Mẹ mua ba giỏ trái cây',
                     'Đường này có hai làn xe', 'đi du lịch Ba Lan về'):
            with self.subTest(text=text):
                self.assertEqual(self.counters(text) + [c.params for c in sv.find_price([self.sentence(text)])], [])
        self.assertEqual(self.counters('Tôi đã thử 3 lần rồi'), [(3, 'lần', None)])

    def test_decomposed_and_partly_composed_input_reads_like_composed(self):
        import unicodedata
        self.assertEqual(vl.normal_value(unicodedata.normalize('NFD', 'bà bạn bán từ đồ')), 'ba ban ban tu đo')
        self.assertEqual(vl.parse_number('hai trie\u0302\u0323u'), 2_000_000)
        price = sv.find_price([self.sentence(unicodedata.normalize('NFD', 'Từ 500 nghìn giảm còn 199 nghìn'))])
        self.assertEqual((price[0].params['price'], price[0].params['old_price']), (199_000, 500_000))

    def test_money_after_a_word_that_is_not_part_of_it(self):
        text = vl.normal_value('Lương tháng mười 15 triệu')
        self.assertEqual([(text[m.start:m.end], m.value) for m in vl.find_money(text)], [('15 vi_trieu', 15_000_000)])
        self.assertEqual(vl.parse_number('hai nghìn lẻ năm'), 2005)

    def test_attached_k_after_one_digit_is_not_money(self):
        for text in ('fiz um video em 4k ontem', 'recebi uma tv 4K de presente'):
            self.assertEqual(vl.find_money(vl.normal_value(text)), [], text)
        self.assertEqual([m.value for m in vl.find_money('500k')], [500_000])

    def test_portuguese_detection_is_unchanged(self):
        self.assertEqual([c.params['keyword'] for c in sv.find_comment([self.sentence('Comenta ROI aqui embaixo que eu te mando')])], ['ROI'])
        for word in ('ve', 'vi', 'tu', 'la', 'roi', 'cai', 'va'):
            self.assertNotIn(word, sv.FUNCTION_WORDS - {'tu'} if word == 'tu' else sv.FUNCTION_WORDS, word)

    def test_portuguese_um_and_ha_are_words_not_fillers(self):
        for word in ('Um', 'um.', 'há', 'Há'):
            self.assertNotIn(assemble_cut.spoken_value(word), assemble_cut.HESITATION, word)
        for word in ('hã', 'ừm', 'Ờ,', 'então'):
            self.assertIn(assemble_cut.spoken_value(word), assemble_cut.HESITATION, word)

    def test_lower_case_accents_do_not_change_the_caption_reach_signature(self):
        self.assertEqual({ch for ch in tr._REACH_ABOVE if ch.islower()}, set('bdfhklt'))

    def test_dong_sign_switches_to_a_font_that_draws_it(self):
        self.assertEqual(tr.font_for_texts('text_bold', ['₫ 500.000']), 'text_bold_extended')
        self.assertEqual(tr.sanitize_text('₫ 500', 'text_bold'), ('đ 500', []))

    def test_rendering_keeps_the_font_captions_were_grouped_with(self):
        cues = {'style': 'clean_caption', 'font': 'text_bold_extended',
                'cues': [{'start': 0.0, 'end': 1.0, 'text': 'video', 'words': [{'text': 'video', 'start': 0.0, 'end': 0.9}]}]}
        self.assertEqual(tr._track_font(cues, 'clean_caption', cues['cues']), 'text_bold_extended')
        self.assertEqual(tr._track_font(dict(cues, font='marker'), 'clean_caption', cues['cues']), 'text_bold')
        self.assertEqual(tr._track_font(dict(cues, style='impact'), 'clean_caption', cues['cues']), 'text_bold')

    def test_template_widths_measure_companion_letters_in_the_companion(self):
        import json
        from PIL import ImageFont
        root = HELPERS.parents[1] / 'engine/project-template/assets/fonts'
        widths = json.loads((root / 'widths.json').read_text(encoding='utf-8'))['fonts']['Caveat']['weights']['700']
        companion = ImageFont.truetype(str(root / 'Sriracha-vietnamese.ttf'), 1000)
        for ch in 'Ạạấếốỵ':
            self.assertEqual(widths[ch], round(companion.getlength(ch)), ch)


if __name__ == '__main__':
    unittest.main()
