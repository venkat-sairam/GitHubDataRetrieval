from src.utils.util import *
from src.logger.logger import logging
from src.exceptions.CustomException import CustomException
from src.entity.configuration_entity import DataIngestionConfiguration
from src.entity.configuration_entity import  TrainingPipelineConfiguration
from src.constants import  timestamp_format, ROOT_DIR
from src.constants.github_data_constants import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
class DataCollectionComponent(object):

    def __init__(self, data_ingestion_configuration: DataIngestionConfiguration) -> None:

        try:
            self.data_ingestion_configuration = data_ingestion_configuration
        except Exception as e:
            raise CustomException(e, sys)

    def read_statewise_usersdata(self )-> pd.DataFrame:
        try:
            return read_from_csv(STATE_WISE_USERSDATA_FILE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

    def filter_repository_data(self, repository) -> pd.DataFrame:
        try:
            test =  [
                {
                "full_repository_name": repo.get('full_name', None),
                "name": repo.get('name', None),
                "user_type":repo.get('owner', {}).get('type', None),

                "created_at":repo.get('created_at', None),
                "pushed_at":repo.get('pushed_at', None),
                "updated_at":repo.get('updated_at', None),

                "default_branch":repo.get('default_branch', None),
                "description":repo.get('description', None),

                "open_issues":repo.get('open_issues', None),
                "open_issues_count":repo.get('open_issues_count', None),

                "visibility":repo.get('visibility', None),
                "watchers":repo.get('watchers', None),
                "watchers_count":repo.get('watchers_count', None),

                "is_disabled":repo.get('disabled', False),
                "is_archieved":repo.get('archived', False),
                "languages_url":repo.get('languages_url', None),
                "contributors_url":repo.get('contributors_url', None)

                } 
                for repo in repository if repo is not None]
            return create_data_frame(test)
        except Exception as e:
            raise CustomException(e, sys)

    def get_contributors_count(self, df, col) ->list:
        try:
            count = []
            if col in df.columns:
                for url in df[col]:
                        if url:
                            res = read_from_url(url)
                            if res.status_code == 200:
                                res = res.json()
                                if res:
                                    if res and isinstance(res, list) and 'contributions' in res[0]:
                                            count.append(res[0]['contributions'])
                                    else:
                                            count.append(0)
                                else:
                                    count.append(0)
                            elif res.status_code == 403: break
                        else: count.append(0)
            while len(count) < len(df):
                count.append(0)
            return count
        except Exception as e:
            raise CustomException(e, sys)

    def get_languages_count(self, df, col):
        try:
            temp = []
            if col in df.columns:
                for url in df[col]:
                    res = read_from_url(url)
                    if res.status_code == 200:
                        res = res.json()
                        if res:
                            temp.append(res)

                    elif res.status_code == 403: break

            return create_data_frame(temp)
        except Exception as e:
            raise CustomException(e, sys)

    def merge_dataframes_row_col_wise(self, df1, df2):
        try:
            t3 = df2.T
            t3.reset_index(inplace=True)
            if 'index' in t3.columns:
                t3.rename(columns={'index': 'language'}, inplace=True)

            languages_long = t3.melt(id_vars='language', var_name='repo_index', value_name='language_count')
            languages_long['repo_index'] = languages_long['repo_index'].astype(int)

            df1 = df1.reset_index().rename(columns={'index': 'index_column'})
            
            merged_df = pd.merge(df1, languages_long, left_on='index_column', right_on='repo_index')

            merged_df.drop('index_column', axis=1, inplace=True)
            merged_df.drop('repo_index', axis=1, inplace=True)
            logging.info(f"merging inside the {currentframe().f_code.co_name}....DONE")

            # current_time_stamp = get_current_time_stamp()

            # dir_path = os.path.join(ROOT_DIR, DATASET_LOCATION, EXTERNAL_DATASET_DIRECTORY_NAME)

            # os.makedirs(dir_path, exist_ok=True)

            # file_name = STATE_WISE_USERSDATA_FILE_NAME

            # write_to_csv(df=merged_df, file_path=join_paths(path1=dir_path, path2=file_name))
            return merged_df
        except Exception as e:
            raise CustomException(e, sys)

    def fetch_repos(self, username, state):

        try:
            repos = read_from_url(f"{USERS_URL}/{username}/repos")
            if repos.status_code == 200:
                repos = repos.json()
                repos.extend([None] * (30 - len(repos)))

                df = self.filter_repository_data(repository=repos)
                df['user name'] = [username] * len(df) 
                df['state'] = [state] * len(df)
                df['contributions_count'] = self.get_contributors_count(df=df, col="contributors_url")
                temp_df = self.get_languages_count(df, 'languages_url')
                merged_df = self.merge_dataframes_row_col_wise(df, temp_df)
                print("Repositories fetched successfully......")
                return False, merged_df
            else:
                raise CustomException(f"Error fetching repositories: Status code {repos.status_code}", sys)
        except Exception as e:
            return True, str(e) 
        
        
    def stratified_sample(self, df, sample_size, random_state=None):
        try:
            state_proportions = df['state'].value_counts(normalize=True)
            state_sample_sizes = np.rint(state_proportions * sample_size).astype(int)

            def sample_from_group(group):
                state = group.name
                n_samples = state_sample_sizes[state]
                return group.sample(n=n_samples, random_state=random_state)

            return df.groupby('state', group_keys=False).apply(sample_from_group)
        except Exception as e:
            raise(CustomException(e, sys))

    def sample_users_data_with_stratified_sampling(self, raw_data_file_path: str, random_state=None):
        try:
            data = read_from_csv(file_path=raw_data_file_path)
            total_records = len(data)
            samples = {percent: {} for percent in SAMPLE_SIZES_PERCENTAGES}

            for percent in SAMPLE_SIZES_PERCENTAGES:
                sample_size = int(total_records * percent)
                samples[percent] = self.stratified_sample(df=data, sample_size=sample_size, random_state=random_state)
            
            directory_location = os.path.join(SAMPLED_USERS_DATASET_FILE_PATH, CURRENT_TIME_STAMP)
            create_directories(directories_path=directory_location)
            processed_dataset_with_time_stamp = directory_location

            for percent in SAMPLE_SIZES_PERCENTAGES:
                path = os.path.join(processed_dataset_with_time_stamp, f"samples_of_size_{int(percent*100)}_percentage.csv")
                write_to_csv(df=samples[percent], file_path=path)
        except Exception as e:
            raise CustomException(e, sys)

        
    def fetch_and_update(self, user_name, state_name):
        # print(f"user_name: {user_name}, state_name: {state_name}")
        exceptionOccurred, df1 = self.fetch_repos(username=user_name, state=state_name)
        if exceptionOccurred:
            return df1, pd.DataFrame()
        return None, df1
            

        return state_name, df1

    def split_dataframe_and_invoke_fetch_repos(self, df,  number_of_sections = 1):
        print("splittting dataframe and invoking the fetch repositories.......")
        try:
            repos_dict = {}
            section_size = len(df) // number_of_sections
            if section_size == 0:
                section_size = 1
            for start in range(0, len(df), section_size):
                end = min(start + section_size, len(df))
                # print(f"start: {start}, end: {end}")
                batch_df = df.iloc[start:end]
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = {executor.submit(self.fetch_and_update, row['username'], row['state']): row for _, row in batch_df.iterrows()}
                    
                    error_detected = False

                    for future in as_completed(futures):
                        exception_message, df1 = future.result()
                        
                        if exception_message:
                            print(f"Error fetching data: {exception_message}")
                            error_detected = True
                            break
                        state_name = df1['state'].iloc[0] if not df1.empty else None
                        if state_name:
                            repos_dict[state_name] = pd.concat([repos_dict.get(state_name, pd.DataFrame()), df1], ignore_index=True)
                    if error_detected: break
                if error_detected: break
                time_delay_seconds = TIME_DELAY_SECONDS 
                wait_time = 3600 / section_size
                if len(df) <=25:
                    wait_time = 5
                print(f"Waiting for {wait_time} seconds")
                time.sleep(wait_time)
                logging.info(f"Time delay for {time_delay_seconds} seconds")
            create_directories(REPOSITORY_DATA_FILE_DIRECTORY_NAME)
            combined_df = pd.DataFrame()
            for state_name, df in repos_dict.items():
                df['state'] = state_name
                combined_df = pd.concat([combined_df, df], ignore_index=True)

            combined_df.to_csv(REPOSITORY_DATA_FILE_PATH, index=False)

        except Exception as e:
            raise CustomException(e, sys)
        
    def download_users_data(self, sample_fraction, file_path: str):
        try:
            self.sample_users_data_with_stratified_sampling(raw_data_file_path=file_path)

            subdirectories = os.listdir(SAMPLED_USERS_DATASET_FILE_PATH)

            subdirectories.sort(reverse=True)
            # print(f"subdirectories in the sampled users folder are: {subdirectories}")

            latest_subdir = subdirectories[0] if subdirectories else None
            filtered_file_name = ""
            try:
                if latest_subdir:
                    search_path = os.path.join(SAMPLED_USERS_DATASET_FILE_PATH, latest_subdir, f"samples_of_size_{sample_fraction}_percentage.csv")
                    
                    for file in glob.glob(search_path):
                        filtered_file_name = file
                        break
                else:
                    raise CustomException(f"No files found in {SAMPLED_USERS_DATASET_FILE_PATH} directory")
            except Exception as e:
                raise CustomException(e, sys)
            print(f"Filtered file name: {filtered_file_name}")
            logging.info(f"Filtered file name: {filtered_file_name}")
            combined_df = read_from_csv(file_path= filtered_file_name)
            # combined_df = combined_df[0:5]
            # print(f"Combined dataframe after using the head function: {combined_df}")
            self.split_dataframe_and_invoke_fetch_repos(df = combined_df, number_of_sections= NUMBER_OF_SECTIONS)
            
            
        except Exception as e:
            raise CustomException(e, sys)

    def  github_users_data_extraction_and_writing_to_csv(self) -> None:
        try:
            
            source_data_directory = self.data_ingestion_configuration.source_data_directory
            os.makedirs(source_data_directory, exist_ok=True)
            print(f"RAW DATA FILE: {RAW_DATASET_FILE_PATH}")
            self.download_users_data(1, RAW_DATASET_FILE_PATH)
            logging.info(f"Created directory at: {source_data_directory}")
                    
        except Exception as e:
            raise CustomException(e, sys)

    def integrate_data_from_processed_csv_files(self, base_directory:str =REPOSITORY_DATA_FILE_DIR_NAME ) -> None:
        all_csv_files = []
        all_dfs = []
        for dir in os.listdir(base_directory):
            dir_path = os.path.join(base_directory, dir)
            # print(f"{dir_path} is the selected data directory")
            if os.path.exists(dir_path):
                csv_files = glob.glob(os.path.join(dir_path, '*.csv'))
                all_csv_files.extend(csv_files)
        
        for file in all_csv_files:
            try:
                if file:
                    all_dfs.append(read_from_csv(file_path=file))
                    print(f"{file} read successfully")
            except Exception as e:
                continue
        
        # # all_dfs = [read_from_csv(file) for file in all_csv_files if file]
        all_dfs = pd.concat(all_dfs)
        print(all_dfs.head())
        # integrated_data_set_location_with_ts = os.path.join(INTEGRATED_DATASET_LOCATION, CURRENT_TIME_STAMP)
        create_directories(directories_path=INTEGRATED_DATASET_LOCATION )        
        write_to_csv(df= all_dfs, file_path= join_paths(INTEGRATED_DATASET_LOCATION,INTEGRATED_DATA_FILE_NAME))


    # def initiate_data_preprocessing(self, data_file:str =join_paths(INTEGRATED_DATASET_LOCATION,INTEGRATED_DATA_FILE_NAME) ):
        df = read_from_csv(file_path=data_file)
        # Removing the duplicate entries from the dataframe.
        logging.info(f"Removing the duplicate entries from the dataframe.")
        print(f"Removing the duplicate entries from the dataframe.")
        df.drop_duplicates(inplace=True)
        
        
        logging.info(f"remvoing the white spaces from column names in the dataset")
        print(f"remvoing the white spaces from column names in the dataset")
        df.columns = [col.replace(" ", "_") for col in df.columns]
        
        logging.info(f"Dropping the unnecessary columns from the dataframe")
        print(f"Dropping the unnecessary columns from the dataframe")
        df.drop(columns=['visibility', 'contributors_url', 'languages_url', 'description', 'name', 'default_branch','full_repository_name'], inplace=True)


        logging.info(f"Dropping the duplicated columns in the dataset")
        print(f"Dropping the duplicated columns in the dataset")
        df.drop(columns=['watchers', 'open_issues'],inplace=True)

        logging.info(f"Filtering the numeric columns present in the dataframe....")
        print(f"Filtering the numeric columns present in the dataframe....")
        numeric_columns = df.select_dtypes(include=['number']).columns

        logging.info(f"Filtering the date-time columns in the dataset")
        print(f"Filtering the date-time columns in the dataset")
        date_columns = ['created_at', 'pushed_at','updated_at' ]

        logging.info(f"Converting created_At, pushed_at, updated_At column values to data-time format")
        print(f"Converting created_At, pushed_at, updated_At column values to date-time format")
        # Coverting the created_At, pushed_at, updated_At to data-time format.
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]) 
        
        logging.info(f"Filterin the categorical columns present in the dataframe")
        print(f"Filterin the categorical columns present in the dataframe")
        # Filtering the categorical columns.
        categorical_columns = [col for col in df.columns if (col  not in numeric_columns) and (col not in date_columns)]
        
        
        print(f"{'='*20}Handling Null values{'='*20}")
        logging.info(f"{'='*20}Handling Null values{'='*20}")

        logging.info(f" Replacing all the null values in numeric columns with ZERO's")
        print(f" Replacing all the null values in numeric columns with ZERO's")
        [df[col].fillna(0, inplace=True) for col in df.columns if col in numeric_columns]
        try:
            [df[col].isnull().any() for col in numeric_columns]
        except ValueError:
            raise CustomException("Null Values exists in the dataframe", sys)
        
        print(f"Handling Null values in the date time columns")
        logging.info(f"{'='*20}Handling Null values in the date time columns{'='*20}")

        for col in date_columns:
            df[col].fillna(method='bfill', inplace=True)

        if not df.isnull().any().any():
            logging.info("Successfully handled all the Null values present in the dataframe... ")
            print(f"{'='*20} >> Successfully handled all the Null values preseent in the dataframe << {'='*20} ")
            preprocessed_data_directory = join_paths(PREPROCESSED_DATASET_DIRECTORY_LOCATION, CURRENT_TIME_STAMP)
            create_directories(directories_path=preprocessed_data_directory)
            preprocessed_data_file_path = join_paths(preprocessed_data_directory,PREPROCESSED_DATA_FILE_NAME)
            write_to_csv(df=df, file_path=preprocessed_data_file_path)
            final_dataset_location= join_paths(FINAL_DATASET_DIRECTORY_LOCATION, PREPROCESSED_DATA_FILE_NAME)
            print(f"Writing the preprocessed dataset to {final_dataset_location}")
            write_to_csv(df=df, file_path=final_dataset_location)
        else:
            logging.error("Null values were not handled successfully...")
            print("Null values were not handled successfully...")



