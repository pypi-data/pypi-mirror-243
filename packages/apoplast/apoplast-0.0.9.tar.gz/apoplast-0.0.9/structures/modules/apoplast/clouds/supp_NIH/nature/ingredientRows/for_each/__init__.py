
'''
	def action (ingredient):
		print (ingredient ["name"]
		return True;

	for_each.start (
		ingredient_rows = ingredientRows,
		action = action
	)
'''

def action (ingredient, indent = 0):
	return True;

def start (
	ingredient_rows = [],
	action = action,
	indent = 0
):
	for ingredient in ingredient_rows:
		advance = action (ingredient, indent = indent)
		if (not advance):
			return;
			
		if ("nestedRows" in ingredient):
			start (
				ingredient_rows = ingredient ["nestedRows"],
				action = action,
				indent = indent + 1
			)

	return;