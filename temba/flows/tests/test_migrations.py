from temba.tests import MigrationTest


class BackfillNewCategoryCountsTest(MigrationTest):
    app = "flows"
    migrate_from = "0354_flowresultcount"
    migrate_to = "0355_backfill_new_cat_counts"

    def setUpBeforeMigration(self, apps):
        self.flow1 = self.create_flow("Flow 1")
        self.flow2 = self.create_flow("Flow 2")

        self.flow1.category_counts.create(
            node_uuid="0043bf6f-f385-4ba3-80d7-4313771efa86",
            result_key="color",
            result_name="Color",
            category_name="Red",
            count=1,
        )
        self.flow1.category_counts.create(
            node_uuid="2c230f54-a7f6-4a71-9f24-b3ba81734552",
            result_key="color",
            result_name="Color",
            category_name="Red",
            count=2,
        )
        self.flow1.category_counts.create(
            node_uuid="0043bf6f-f385-4ba3-80d7-4313771efa86",
            result_key="color",
            result_name="Color",
            category_name="Blue",
            count=4,
        )
        self.flow1.category_counts.create(
            node_uuid="f27d77e9-4ccb-4c36-8277-f5708822cf26",
            result_key="name",
            result_name="Name",
            category_name="All Responses",
            count=6,
        )
        self.flow2.category_counts.create(
            node_uuid="daf35e03-b82e-4c12-8ff7-60f7d990eb05",
            result_key="thing",
            result_name="Thing",
            category_name="Looooonnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnggggggggggggnnggggggggggggggggg",
            count=2,
        )
        self.flow2.category_counts.create(
            node_uuid="daf35e03-b82e-4c12-8ff7-60f7d990eb05",
            result_key="thing",
            result_name="Thing",
            category_name="Zero",
            count=0,
        )

    def test_migration(self):
        def assert_counts(flow, expected):
            actual = {}
            for count in flow.result_counts.all():
                actual[f"{count.result}/{count.category}"] = count.count

            self.assertEqual(actual, expected)

        assert_counts(self.flow1, {"color/Red": 3, "color/Blue": 4, "name/All Responses": 6})
        assert_counts(self.flow2, {"thing/Looooonnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnggggggggggggnngggggggggg": 2})
