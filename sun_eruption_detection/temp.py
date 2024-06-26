# Part 1
# t_start = time.parse_time(np_rec_array[0][1], format="utime").to_datetime()
# t_peak = time.parse_time(np_rec_array[0][3], format="utime").to_datetime()
# t_end = time.parse_time(np_rec_array[0][2], format="utime").to_datetime()
# n_points = np_rec_array[0][6]
# x_start, y_start = np_rec_array[0][12], np_rec_array[0][15]
# # ---------------------------------------------------------
# # narrow_image_quantity(np_rec_array) # adjust the image quantity from heliover to eruptivesun
#
# x_center = np_rec_array[0]["X_CENTER"]
# y_center = np_rec_array[0]["Y_CENTER"]
#
# x_center = x_center[x_center != 0]
# y_center = y_center[y_center != 0]


# Part 2
# horizontal_joined_images = np.concatenate([image_area_map[biggest_area]], axis=1)
# cv.imshow("images", resized_img)
# cv.waitKey()
# cv.imwrite(str(BASE_PATH / "subtracted_and_countered_areas.jp2"), horizontal_joined_images)

# for image_path in NARROWED_IMAGES_PATH.iterdir():
#     jp2 = cv.imread(str(image_path))  # , flags=cv.IMREAD_GRAYSCALE
#
#     headers = get_header(str(image_path))[0]
#     x_img_center, y_img_center = headers["X0_MP"], headers["Y0_MP"]
#     pixel_scale = headers["IMSCL_MP"]
#
#     for x_sav, y_sav in zip(x_center, y_center, strict=True):
#         x = x_sav / pixel_scale
#         y = y_sav / pixel_scale
#
#         new_x, new_y = int(x_img_center + x), int(y_img_center - y)
#         cv.circle(jp2, (new_x, new_y), 5, (255, 0, 0), thickness=5)
#     resized_jp2 = cv.resize(jp2, (1024, 1024), interpolation=cv.INTER_AREA)
#     cv.imshow("img", resized_jp2)
#     cv.waitKey(0)

# resized_jp2_1 = cv.resize(jp2_1, (512, 512), interpolation=cv.INTER_AREA)
# resized_jp2_2 = cv.resize(jp2_2, (512, 512), interpolation=cv.INTER_AREA)
# resized_subs_res = cv.resize(subs_res, (512, 512), interpolation=cv.INTER_AREA)
# # inverted_resized_subs_res = np.invert(resized_subs_res)
#
# horizontal = np.concatenate((resized_jp2_1, resized_jp2_2, resized_subs_res), axis=1)
#
# cv.imshow("Sun Eruption", horizontal)
# cv.waitKey(0)
#
# for image_path, x_sav, y_sav in zip(NARROWED_IMAGES_PATH.iterdir(), x_center, y_center, strict=True):
#     # TODO -> get the event coordinates and apply them to the formula
#     #  Pixel Position = (Angular Measurement / Pixel Scale) * (Focal Length / 206.265)
#     jp2 = cv.imread(str(image_path))
#     headers = get_header(image_path)[0]
#     x_img_center, y_img_center = headers["X0_MP"], headers["Y0_MP"]
#     pixel_scale = headers["IMSCL_MP"]
#
#     x = x_sav / pixel_scale
#     y = y_sav / pixel_scale
#
#     new_x, new_y = int(x_img_center + x), int(y_img_center - y)
#     print(f"x: {x}, y: {y}")
#     # TODO -> why 125 had to be added to adjust the event position?
#     cv.circle(jp2, (new_x, new_y), 200, (255, 0, 0), thickness=5)  # x + 125
#     cv.circle(jp2, (new_x, new_y), 10, (255, 0, 0), thickness=5)  # x + 125
#     resized_jp2 = cv.resize(jp2, (1024, 1024), interpolation=cv.INTER_AREA)
#
#     cv.imshow("Sun Eruption", resized_jp2)
#     cv.waitKey(0)
# os.chdir(MARKED_IMAGES_PATH)
# cv.imwrite(image_path.name, jp2)

#     if name == "TIMES":
#         for sav_time in value:
#             converted_sav_time = time.parse_time(sav_time, format="utime").to_datetime()
#             if converted_sav_time.year != 1970:
#                 print(converted_sav_time)

# def get_image_path_by_date(image_dt: dt.datetime) -> Path:
#     return IMAGES_PATH / f"{image_dt.strftime('%Y_%m_%d__%H_%M_%S_%f')}_SDO_AIA_AIA_171.jp2"

# def find_white_areas() -> None:
#     img_path_1 = list(NARROWED_IMAGES_PATH.iterdir())[0]
#     img_path_2 = list(NARROWED_IMAGES_PATH.iterdir())[15]
#
#     img_1 = cv.imread(str(img_path_1))
#     img_2 = cv.imread(str(img_path_2))
#
#     subs_res = cv.subtract(img_1, img_2)
#     gray = cv.cvtColor(subs_res, cv.COLOR_BGR2GRAY)
#     thresh = cv.threshold(gray, 16, 255, cv.THRESH_BINARY)[1]
#
#     cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
#     min_area = 0.1  # 15000
#     white_dots = []
#     for c in cnts:
#         area = cv.contourArea(c)
#         if area > min_area:
#             cv.drawContours(subs_res, [c], -1, (36, 255, 12), 2)
#             white_dots.append(c)
#
#     print("White Dots count is:", len(white_dots))
#     resized_img_1 = cv.resize(img_1, (768, 768), interpolation=cv.INTER_AREA)
#     resized_img_2 = cv.resize(img_2, (768, 768), interpolation=cv.INTER_AREA)
#     resized_subs_res = cv.resize(subs_res, (768, 768), interpolation=cv.INTER_AREA)
#     horizontal_joined_images = np.concatenate((resized_img_1, resized_img_2, resized_subs_res), axis=1)
#     cv.imshow("images", horizontal_joined_images)
#     cv.waitKey()

# img_path_1 = list(NARROWED_IMAGES_PATH.iterdir())[0]
    # img_1 = cv.imread(str(img_path_1))
    #
    # headers = get_header(str(img_path_1))[0]
    # sun_radius = headers["R_SUN"] - 400
    # x_img_center, y_img_center = headers["X0_MP"], headers["Y0_MP"]
    #
    # image_area_map = {}
    # min_area = 100
    # for idx, img_path in enumerate(list(NARROWED_IMAGES_PATH.iterdir())[1:]):
    #     img_2 = cv.imread(str(img_path))
    #
    #     subs_res = cv.subtract(img_1, img_2)  # image subtraction
    #     gray = cv.cvtColor(subs_res, cv.COLOR_BGR2GRAY)  # rgb -> greyscale
    #     thresh = cv.threshold(gray, 16, 255, cv.THRESH_BINARY)[1]  # threshold (obtain binary image)
    #
    #     contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # contour the thresholded image
    #     contours = contours[0] if len(contours) == 2 else contours[1]
    #
    #     max_area = max([cv.contourArea(contour) for contour in contours])
    #     min_area = (
    #         max_area // 2
    #     )  # Excluding smaller contoured areas. The scale of increase for this variable differs for each eruption case
    #     white_spots = []
    #     for contour in contours:
    #         area = cv.contourArea(contour)
    #         if area > min_area:
    #             cv.circle(
    #                 subs_res,
    #                 (int(x_img_center), int(y_img_center)),
    #                 int(sun_radius),
    #                 (255, 0, 0),
    #                 thickness=5,
    #             )
    #             image_area_map[area] = subs_res
    #             white_spots.append(contour)
    #
    #             coordinates = get_outside_pixels(x_img_center, y_img_center, sun_radius, contour)
    #
    #             if coordinates.any():
    #                 cv.drawContours(img_2, [np.expand_dims(coordinates, axis=1)], -1, (36, 255, 12), 4)
    #
    #             resized_img_2 = cv.resize(img_2, (1024, 1024), interpolation=cv.INTER_AREA)
    #             cv.imshow("image", resized_img_2)
    #             cv.waitKey(1)
    #
    #     print(f"White Dots count is: {len(white_spots)}, max_area: {max_area}, min_area: {min_area}, image: {idx+1}")
