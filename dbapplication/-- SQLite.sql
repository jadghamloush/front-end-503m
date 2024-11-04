-- Sub-categories for Shorts (bottoms_id = 1)
INSERT INTO bottoms_subcategories (
        bottoms_id,
        type,
        price,
        size,
        quantity,
        for_gender
    )
VALUES (1, 'Casual Shorts', 20.0, 'M', 15, 'Men'),
    (1, 'Running Shorts', 25.0, 'S', 10, 'Women'),
    (1, 'Kids Shorts', 15.0, 'L', 15, 'Kids');
-- Sub-categories for Sweatpants (bottoms_id = 2)
INSERT INTO bottoms_subcategories (
        bottoms_id,
        type,
        price,
        size,
        quantity,
        for_gender
    )
VALUES (2, 'Regular Sweatpants', 30.0, 'M', 10, 'Men'),
    (2, 'Jogger Sweatpants', 35.0, 'L', 10, 'Women'),
    (2, 'Kids Sweatpants', 25.0, 'S', 10, 'Kids');
-- Sub-categories for Leggings (bottoms_id = 3)
INSERT INTO bottoms_subcategories (
        bottoms_id,
        type,
        price,
        size,
        quantity,
        for_gender
    )
VALUES (3, 'Athletic Leggings', 40.0, 'M', 10, 'Women'),
    (3, 'Yoga Leggings', 45.0, 'S', 8, 'Women'),
    (3, 'Kids Leggings', 30.0, 'L', 7, 'Kids');