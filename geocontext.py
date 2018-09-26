# geocontext.py
# Pontus Hennerdal
# September 26, 2018

def kNearest_context(points_DataFrame,
                     popLocations_DataFrame,
                     group_List,
                     pop_Column,
                     kValue_List,
                     points_NorthColumn='North',
                     points_EastColumn='East',
                     popLocations_NorthColumn='North',
                     popLocations_EastColumn='East'):
    """This function calculate the geographical context around each point in the points_DataFrame. The context is the proportion of the population among the k-nearest neighbours in the popLocations_DataFrame that is part of a group. Distance is measured as the Euclidean distance."""
    
    # To make sure the k-values are listed ascending, the list with k-values is sorted.
    kValue_List.sort()
    
    # Creating space in the points_DataFrame for radius, total, and group count for every k-value.
    for kValue in kValue_List:
        points_DataFrame['radius_k'+str(kValue)] = 0
        points_DataFrame['total_k'+str(kValue)] = 0
        for group in group_List:
            points['group_'+group+'_k'+str(kValue)] = 0
    
    # Creating space in the popLocations_DataFrame for distance to a point. This column will be changed for every point in points_DataFrame.
    popLocations_DataFrame['Distance'] = 0
    
    # For every point in points_DataFrame.
    for pointIndex in range(len(points_DataFrame)):
        # Find the coordinates for the point
        North0 = points_DataFrame[points_NorthColumn].iloc[pointIndex]
        East0 = points_DataFrame[points_EastColumn].iloc[pointIndex]
        
        # Calculate the Euclidean distance from the point to every populated location in popLocations_DataFrame.
        popLocations_DataFrame['Distance'] = np.sqrt(np.power(North0-popLocations_DataFrame[popLocations_NorthColumn], 2) + np.power(East0-popLocations_DataFrame[popLocations_EastColumn], 2)).astype('int')
        
        # Sort populated locations by distance to the point.
        popLocations_DataFrame.sort_values('Distance', inplace=True)
        
        # Set start values for every point.
        radius_List = []
        population = 0
        index = 0
        
        # Going through every k-value in the list. 
        for kValue in kValue_List:
            # While the poplation is lower than the k-value
            while population < kValue:
                # Add the population of that populated location
                population += popLocations_DataFrame[pop_Column].iloc[index]
                index += 1
            
            # When the population is larger than the k-value: save the radius to the radius_List.
            radius = popLocations_DataFrame['Distance'].iloc[index-1]
            radius_List.append(radius)
            points_DataFrame['radius_k'+str(kValue)].iat[pointIndex] = radius

        # When the the max radius for all k-values are found: go through every k-value in the list again.
        for k_Index in range(len(kValue_List)):
            # For each k-value, select all populated locations upp to the previous found max distance.
            selection = popLocations_DataFrame[popLocations_DataFrame['Distance'] <= radius_List[k_Index]]
            
            # For each group, calculate the sum of that group among the selected nearest neighbours.
            for group in group_List:
                points_DataFrame['group_'+group+'_k'+str(kValue_List[k_Index])].iat[pointIndex] = selection[group].sum()
            
            # Calculate the sum of selected nearest neighbours
            points_DataFrame['total_k'+str(kValue_List[k_Index])].iat[pointIndex] = selection[pop_Column].sum()

    # Calculate the proportion those groups are of the total amount of neighbours.
    for kValue in kValue_List:
        for group in group_List:
            points_DataFrame['prop_'+group+'_k'+str(kValue)] = points_DataFrame['group_'+group+'_k'+str(kValue)]/points_DataFrame['total_k'+str(kValue)]
    
    # The function returns points_DataFrame with the added columns.
    return points_DataFrame
