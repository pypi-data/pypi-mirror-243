""" Some Maths
"""


import numpy as np
import pandas as pd



def df_with_slops_and_angles(df, x1_col, x2_col, y1_col, y2_col):
	"""add the dataframe with slop and angle for the given co-ordinates on plane.

	Args:
		df (DataFrame): Input DataFrame
		x1_col (str): column name for point 1 - x axis
		x2_col (str): column name for point 2 - x axis
		y1_col (str): column name for point 1 - y axis
		y2_col (str): column name for point 2 - y axis

	Returns:
		DataFrame: Updated Output DataFrame
	"""	
	df['slop'] = (df[y2_col] - df[y1_col])/(df[x2_col] - df[x1_col])
	df = df.fillna("")
	df['angle_angled_connector'] = df.slop.apply(slop_to_angled_connector)
	df['angle_straight_connector'] = df.slop.apply(slop_to_straight_connector)
	return df.fillna("")


def slop_to_straight_connector(m):
	"""calculate angle from given slop(m) of a straight line.

	Args:
		m (float): slop of a straight line

	Returns:
		int: degree/slop of line
	"""		
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 90+angle
	if m <= 0: angle = 360-angle 
	return angle

def slop_to_angled_connector(m):
	"""calculate angle from given slop(m) of an angled line.

	Args:
		m (float): slop of an angled line

	Returns:
		int: degree/slop of line
	"""		
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 180-angle
	if m > 0: angle = 360-angle 
	return angle




# --------------------------------------------- 
# Co-ordinate calculator
# --------------------------------------------- 
class CalculateXY():
	"""Co-ordinate calculator
	"""	
	def __init__(self, dev_df, default_x_spacing, default_y_spacing, cbl_df, sheet_filter_dict):
		"""initialize object by providing device DataFrame, default x & y - axis spacing values.

		Args:
			dev_df (DataFrame): Device DataFrame
			default_x_spacing (int, float): horizontal spacing between two devices
			default_y_spacing (int, float): vertical spacing between two devices
			cbl_df (DataFrame): Cabling DataFrame
			sheet_filter_dict (dict): sheet filters for multi tab drawing
		"""		
		self.df = dev_df
		self.cbl_df = cbl_df
		#
		self.spacing_x = default_x_spacing
		self.spacing_y = default_y_spacing
		#
		self.sheet_filter_dict = sheet_filter_dict


	def calc(self):
		"""calculation sequences
		"""		
		self.sort()
		ho_dict = self.count_of_ho(self.df)
		#
		self.update_ys(self.df, 'y-axis', ho_dict)
		self.update_xs(self.df, 'x-axis', ho_dict)
		#
		self.update_xy_for_sheet_filter_dict()
		self.merge_xy_filter_dfs_with_dev_df()


	def update_xy_for_sheet_filter_dict(self):
		"""create and calculate x-axis, y-axis columns, values for each filtered tab database
		"""		
		self.sheet_filter_cbl_df_dict = {}
		self.sheet_filter_dev_df_dict = {}
		self.sheet_filter_dev_dict = {}
		for k, v in self.sheet_filter_dict.items():
			self.sheet_filter_cbl_df_dict[k] = self.cbl_df[self.cbl_df[k] == v] 
			self.sheet_filter_dev_dict[k] = set(self.sheet_filter_cbl_df_dict[k]['a_device']).union(set(self.sheet_filter_cbl_df_dict[k]['b_device']))
			self.sheet_filter_dev_df_dict[k] = self.df[self.df.hostname.apply(lambda x: x in self.sheet_filter_dev_dict[k])]
			ho_dict = self.count_of_ho(self.sheet_filter_dev_df_dict[k])
			self.update_ys(self.sheet_filter_dev_df_dict[k], f'{k}-y-axis', ho_dict)
			self.update_xs(self.sheet_filter_dev_df_dict[k], f'{k}-x-axis', ho_dict)
			self.sheet_filter_dev_df_dict[k] = self.sheet_filter_dev_df_dict[k][['hostname', f'{k}-x-axis', f'{k}-y-axis']]

	def merge_xy_filter_dfs_with_dev_df(self):
		"""merge sheet filter x,y column information with main device dataframe
		"""		
		for k, v in self.sheet_filter_dev_df_dict.items():
			self.df = self.df.join(v.set_index('hostname'), on='hostname')


	def sort(self):
		"""sort the Device DataFrame based on ['hierarchical_order', 'hostname']
		"""		
		self.df.sort_values(by=['hierarchical_order', 'hostname'], inplace=True)
		self.df = self.df[self.df.hierarchical_order != 100]

	def count_of_ho(self, df):
		"""counts hierarchical_order items for given dataframe and stores it in local dict 

		Args:
			df (DataFrame): Device Dataframe with `hierarchical_order` column

		Returns:
			_type_: _description_
		"""		
		vc = df['hierarchical_order'].value_counts()
		return {ho: c for ho, c in vc.items()}

	def calc_ys(self, ho_dict):
		"""calculate y-axis refereances with respect to high order dictionary

		Args:
			ho_dict (dict): high order devices dictionary

		Returns:
			dict: high order dictionary with y-axis reference values
		"""		
		ih, y = 0, {}
		for i, ho in enumerate(sorted(ho_dict)):
			if i == 0: 
				y[ho] = ih
				prev_ho = ho
				continue
			c = ho_dict[ho] + ho_dict[prev_ho]
			ih += c/2 * self.spacing_y
			y[ho] = ih
		y = self.inverse_y(y)
		return y

	def inverse_y(self, y):
		"""inverses the y axis values (turn upside down)

		Args:
			y (dict): dictionary with y axis placement values based on hierarchical_order

		Returns:
			dict: inversed dictionary with y axis placement values based on reversed hierarchical_order
		"""
		return {k: max(y.values()) - v+2 for k, v in y.items()}

	def get_y(self, ho): 
		"""get the y axis value for the given hierarchical_order

		Args:
			ho (int): hierarchical order number

		Returns:
			int, float: y axis value
		"""		
		return self.y[ho]

	def update_ys(self, df, y_axis, ho_dict):
		"""update  `y-axis` column to given `df` Device DataFrame

		Args:
			df (DataFrame): Device DataFrame
			y_axis (str): column name for y_axis
			ho_dict (dict): high order devices dictionary
		"""			
		self.y = self.calc_ys(ho_dict)
		df[y_axis] = df['hierarchical_order'].apply(self.get_y)

	# -----------------------------------------------

	def get_x(self, ho): 
		"""get the x axis value for a device from given hierarchical order number

		Args:
			ho (int): hierarchical order number

		Returns:
			int, float: x axis value
		"""		
		for v in sorted(self.xs[ho]):
			value = self.xs[ho][v]
			break
		del(self.xs[ho][v])
		return value

	def calc_xs(self, ho_dict):
		"""calculate x-axis refereances with respect to high order dictionary

		Args:
			ho_dict (dict): high order devices dictionary

		Returns:
			dict: high order dictionary with x-axis reference values
		"""		
		xs = {}
		middle = self.full_width/2
		halfspacing = self.spacing_x/2
		for ho in sorted(ho_dict):
			if not xs.get(ho):
				xs[ho] = {}
			c = ho_dict[ho]
			b = middle - (c/2*self.spacing_x) - halfspacing
			for i, x in enumerate(range(c)):
				pos = x*self.spacing_x + b 
				xs[ho][i] = pos
		return xs

	def update_xs(self, df, x_axis, ho_dict):
		"""update  `x-axis` column to given `df` Device DataFrame

		Args:
			df (DataFrame): Device DataFrame
			x_axis (str): column name for x_axis
			ho_dict (dict): high order devices dictionary
		""" 	
		self.full_width = (max(ho_dict.values())+2) * self.spacing_x
		self.xs = self.calc_xs(ho_dict)
		df[x_axis] = df['hierarchical_order'].apply(self.get_x)


# --------------------------------------------- 

