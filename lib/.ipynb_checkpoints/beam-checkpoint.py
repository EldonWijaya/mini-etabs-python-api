from . import csiapi

# Assinging locations to beams
def assign_beam_stations(df, cantilever_prefix = 'CL', girder_prefix = 'G', beam_prefix = 'B'):
    
    beam_unique_name = df['UniqueName']
    beam_station = df['Station']
    beam_design_sect = df['DesignSect']
    try:
        beam_as_top = df['AsTopTotal'] # for cantilever checking
    except:
        pass    
    max_station = []
    min_station = []
    ln = []
    reinforcement_location = []
    for idx in range(len(beam_unique_name)):
    # for i in range(1):
        i = beam_unique_name[idx]
        local_beam_station = beam_station[idx]
        local_design_sect = beam_design_sect[idx]
        local_beam_stations = (beam_station[i == beam_unique_name]).to_numpy()
        # max_station[i] = max(local_beam_stations)
        # min_station[i] = min(local_beam_stations)
        local_max_station = max(local_beam_stations)
        local_min_station = min(local_beam_stations)
        local_ln = local_max_station - local_min_station
        max_station.append(local_max_station)
        min_station.append(local_min_station)
        # max_station.concatenate(local_max_station)
        # min_station.concatenate(local_min_station)
        ln.append(local_max_station-local_min_station)
        if cantilever_prefix in local_design_sect:
            local_beam_as_top = (beam_as_top[i == beam_unique_name]).to_numpy()
            condition1 = local_beam_as_top[0] > local_beam_as_top[-1]
            condition2 = local_beam_station <= (local_ln / 2 + local_min_station)
            # if condition1 & condition2:
            #    local_location = 'End'
            if ~(condition1 ^ condition2):
                local_location = 'End'
            else:
                local_location = 'Mid'
        elif (girder_prefix in local_design_sect) | (beam_prefix in local_design_sect):
            if local_beam_station < (1/4*local_ln + local_min_station):
                local_location = 'End-I'
            elif local_beam_station > (3/4*local_ln + local_min_station):
                local_location = 'End-J'
            else:
                local_location = 'Mid'
        reinforcement_location.append(local_location)
        # ln.concatenate(local_max_station-local_min_station)
    df['Location'] = reinforcement_location
    return df

def extract_base(data_string):
    # Split the string by hyphen and join all parts except the last one
    parts = data_string.split('-')
    base_string = '-'.join(parts[:-1])
    return base_string

def remove_beam_labels(SapModel, remove_sections = True):
    SapModel.SetModelIsLocked(False)
    frame_assignments_table = csiapi.get_table_display(SapModel, 'Frame Assignments - Summary')
    
    for i in frame_assignments_table.iterrows():
        _, i = i
        new_section = extract_base(i['Analysis Section'])
        SapModel.FrameObj.SetSection(str(i['UniqueName']), extract_base(str(i['Analysis Section'])))

    if remove_sections:
        frame_sections_table = csiapi.get_table_display(SapModel, 'Frame Section Property Definitions - Summary')
        for i in frame_sections_table.iterrows():
            _, i = i
            if '-' in i['Name']:
                SapModel.PropFrame.Delete(i['Name'])
    
