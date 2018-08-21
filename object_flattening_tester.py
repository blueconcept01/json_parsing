import unittest
import json
import object_flattening.flattener as flattener


class FlattenerTester(unittest.TestCase):

    def test_flatten(self):
        with open("files/restaurants.json") as f:
            d = json.load(f)
            flatter = flattener.ObjectFlattener()
            flatter.flatten(d)
            actual = flatter.flatten_dict_list
            with open("test_files/restaurants/restaurant") as r_f:
                d_restaurants = json.load(r_f)
                self.assertListEqual(d_restaurants, actual["restaurant"])
            with open("test_files/restaurants/restaurant_address") as r_a_f:
                d_restaurant_addresses = json.load(r_a_f)
                d_restaurant_addresses[0]['coord'] = '[-73.856077, 40.848447]'
                self.assertListEqual(d_restaurant_addresses, actual["restaurant_address"])
            with open("test_files/restaurants/restaurant_grade") as r_f_g:
                d_restaurant_grades = json.load(r_f_g)
                d_restaurant_grades = [{clean_str(k): clean_str(v) for k, v in n.items()}for n in d_restaurant_grades]
                self.assertListEqual(d_restaurant_grades, actual["restaurant_grade"])
            with open("test_files/restaurants/restaurant_grade_score") as r_f_g_s:
                d_restaurant_grade_scores = json.load(r_f_g_s)
                d_restaurant_grade_scores = [{clean_str(k): clean_str(v) for k, v in n.items()}
                                             for n in d_restaurant_grade_scores]
                self.assertListEqual(d_restaurant_grade_scores, actual["restaurant_grade_score"])

    def test_strip_s(self):
        self.assertEqual(flattener.strip_s("addresses"), "address")
        self.assertEqual(flattener.strip_s("address"), "address")
        self.assertEqual(flattener.strip_s("restaurants"), "restaurant")
        self.assertEqual(flattener.strip_s("s"), "s")
        self.assertEqual(flattener.strip_s("es"), "e")

    def test_combine_words(self):
        self.assertEqual(flattener.combine_words("", "a"), "a")
        self.assertEqual(flattener.combine_words("b", ""), "b")
        self.assertEqual(flattener.combine_words("b", "a"), "b_a")
        self.assertEqual(flattener.combine_words("", ""), "")

    def test_is_data(self):
        self.assertTrue(flattener.is_data("abc"))
        self.assertTrue(flattener.is_data(1))
        self.assertTrue(flattener.is_data(3.41))
        self.assertTrue(flattener.is_data(["abc"]))
        self.assertFalse(flattener.is_data({1: 2}))
        self.assertFalse(flattener.is_data([{1: 2}]))


def clean_str(s):
    return s.replace("Â\xad", "-")
