def process(cv_image, orb, des2):

	kp1 = orb.detect(cv_image,None)
	kp1, des1 = orb.compute(cv_image, kp1)
	#img_ = cv2.drawKeypoints(cv_image, kp1,None, color=(0,255,0), flags=0)
	#cv2.imshow("Image window", img_)
	#cv2.waitKey(3)

	#(rows,cols,channels) = cv_image.shape
	#if cols > 60 and rows > 60 :
	#  cv2.circle(cv_image, (50,50), 10, 255)

	#ref_ = cv2.drawKeypoints(ref, kp2,None, color=(0,255,0), flags=0)
	#cv2.imshow("Image window", ref_)
	#cv2.waitKey(3)

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	matches = bf.match(des1, des2)
	matches = sorted(matches, key = lambda x:x.distance)
	# print(len(matches), len(des1), len(des2))
	# dist = [matches[i].distance for i in range(min(10,len(matches)))]
	dist = [matches[i].distance for i in range(min(10,len(matches)))]
	# print(">>>" , dist)

	cv_image_idxs = [mat.queryIdx for mat in matches]
	ref_idxs = [mat.trainIdx for mat in matches]

	if len(dist)==0: avg_dist = 100
	else: avg_dist = sum(dist)/len(dist)
	# print("dist= ", avg_dist)

	img_ = cv_image
	if avg_dist < 40.0:
		print(avg_dist)
		# img_ = cv2.drawKeypoints(cv_image, [kp1[cv_image_idxs[i]] for i in range(min(10,len(matches)))], None, color=(0,255,0), flags=0)
		img_ = cv2.drawKeypoints(cv_image, kp1, None, color=(0,255,0), flags=0)
		X = []
		Y = []
		# for i in range(min(10,len(matches))):
		for i in range(len(matches)):
			(x,y) = kp1[cv_image_idxs[i]].pt
			X = X + [x]
			Y = Y + [y]
		x_mid = sum(X)/len(X)
		y_mid = sum(Y)/len(Y)
		# print("!!!!",len(X),len(Y))
		cv2.circle(img_, (int(x_mid),int(y_mid)), 10, 150)
		cv2.circle(img_, (math.floor(x),math.floor(y)), 10, 255)
	img_ = cv2.drawKeypoints(cv_image, kp1, None, color=(0,255,0), flags=0)

	cv2.imshow("Image window", cv_image)
	cv2.waitKey(3)
