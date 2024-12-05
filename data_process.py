
import pandas as pd 
import os

def process_experiment_data(directory_path, output_file):
    all_data = []
    participant_accuracies = []
    
    def map_condition(row):
        condition_map = {
            'a': 'M_ref',
            'b': 'L_ref',
            'c': 'M_pred',
            'd': 'L_pred',
            'e': 'M_ref_O',
            'f': 'L_ref_O' if row['Class'] == 1 else 'filler'
        }
        return condition_map.get(row['Type'], row['Type'])
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)
            
            trial_data = df[df['ex_trials.thisN'].notna()]
            
            participant_num = int(trial_data['participant'].iloc[0])
            list_num = (participant_num % 6) + 1
            
            # Calculate accuracy rate
            accuracy = trial_data['key_resp_3.corr'].mean() * 100
            participant_accuracies.append({
                'participant': participant_num,
                'accuracy_rate': accuracy
            })
            
            trial_data['List'] = list_num
            trial_data['reading_time_ms'] = trial_data['reading_time.rt'] * 1000
            trial_data['Condition'] = trial_data.apply(map_condition, axis=1)
            
            relevant_data = trial_data[[
                'participant', 
                'external_id', 
                'List', 
                'ItemIdx',
                'TargetS',
                'Condition',
                'reading_time_ms',
                'key_resp_3.corr'
            ]]
            
            all_data.append(relevant_data)
    
    # Combine all participant data
    combined_data = pd.concat(all_data, ignore_index=True)
    
    # Create accuracy dataframe
    accuracy_df = pd.DataFrame(participant_accuracies)
    
    # Save main data
    combined_data.to_csv(output_file, index=False)
    
    # Save accuracy data
    accuracy_file = output_file.replace('.csv', '_accuracy.csv')
    accuracy_df.to_csv(accuracy_file, index=False)
    
    return combined_data, accuracy_df

# Usage:
# directory = "path/to/your/csv/files"
# output = "combined_data.csv"
# data, accuracies = process_experiment_data(directory, output)

process_experiment_data("/Users/shinyan/Desktop/MetRef 09:2024/online experiment/data/preliminary_18 data/data", "combined_data.csv")