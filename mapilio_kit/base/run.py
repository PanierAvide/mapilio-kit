import os
import getpass

from upload import upload, zip_images
from edit_config import edit_config
from process_csv_to_description import process_csv_to_description


class Run:
    name = "run"
    # TODO: change help
    help = "Mapilio"

    def __init__(self):
        from . import authenticator
        from . import uploader
        from . import video_loader
        from . import decomposer
        from . import image_and_csv_uploader
        from . import Zipper
        self.authenticator = authenticator()
        self.uploader = uploader()
        self.video_loader = video_loader()
        self.decomposer = decomposer()
        self.image_and_csv_uploader = image_and_csv_uploader()
        self.zipper = Zipper()
        self.video_sample_interval = 1
        self.interpolate_directions = True

    def fundamental_arguments(self, parser):
        group = parser.add_argument_group("run options")

    def check_auth(self):
        user_name = input("Enter your username: ").strip()
        user_email = input("Enter your email: ").strip()
        user_password = getpass.getpass("Enter Mapilio user password: ").strip()

        if user_name and user_email and user_password:
            args = self.get_args(edit_config)
            args["user_name"] = user_name
            args["user_email"] = user_email
            args["user_password"] = user_password
            return self.authenticator.perform_task(args)

        else:
            print("Please enter your username, email and password properly \n\n\n\n\n")
            self.check_auth()

    def perform_image_upload(self):
        args = self.get_args(upload)
        import_path = input("Enter your image path: ").strip()
        processed = input("Are your images processed already [y,Y,yes,Yes]?").strip()

        if import_path and processed:
            args["import_path"] = import_path

            if processed not in ["y", "Y", "yes", "Yes"]:
                args["processed"] = False
            else:
                args["processed"] = True

            return self.uploader.perform_task(args)

        else:
            print("Please enter your image path and processed properly \n\n\n\n\n")
            self.perform_image_upload()

    def panorama_image_upload(self):
        args = self.get_args(process_csv_to_description)
        import_path = input("Enter your image path: ").strip()
        csv_path = input("Enter your csv path: ").strip()

        if import_path and csv_path:
            args["import_path"] = import_path
            args["csv_path"] = csv_path
            args["processed"] = False

            return self.image_and_csv_uploader.perform_task(args)

        else:
            print("Please enter your image and csv path properly \n\n\n\n\n")
            self.panorama_image_upload()

    def perform_decompose(self):
        args = self.get_args(edit_config)
        import_path = input("Enter your image path: ").strip()

        if import_path:
            args["import_path"] = import_path
            return self.decomposer.perform_task(args)
        else:
            print("Please enter your image path properly \n\n\n\n\n")
            self.perform_decompose()

    def perform_video_upload(self):
        args = self.get_args(upload)
        video_import_path = input("Enter your video path: ").strip()
        processed = input("Are your images processed already [y,Y,yes,Yes]?").strip()
        if video_import_path:
            import_path = '/'.join(video_import_path.split('/')[:-1]) + '/' + 'images' + '/'
            args["import_path"] = import_path
            if processed not in ["y", "Y", "yes", "Yes"]:
                args["video_import_path"] = video_import_path
                geotag_source = input(
                    "Enter your geotag source (choices=['exif', 'gpx', 'gopro_videos', 'nmea']): ").strip()
                # self.video_sample_interval = int(input("Enter your video sample interval: ").strip())
                args["processed"] = False
                args["geotag_source"] = geotag_source
                args["interpolate_directions"] = self.interpolate_directions
                args["video_sample_interval"] = self.video_sample_interval
                return self.video_loader.perform_task(args)


            else:
                # desc_path = input("Enter your description json path: ").strip()
                # args["desc_path"] = desc_path
                args["processed"] = True
                return self.uploader.perform_task(args)


        else:
            print("Please enter your video path properly \n\n\n\n\n")
            self.perform_video_upload()

    def gopro360max_upload(self):
        pass

    def zip_upload(self):
        args = self.get_args(zip_images)
        import_path = input("Enter your image path: ").strip()
        zip_dir = import_path
        if import_path:
            args["import_path"] = import_path
            args["zip_dir"] = zip_dir
            args["processed"] = False
            check_zip = self.zipper.perform_task(args)
            if check_zip:
                zip_file_path = \
                [os.path.join(zip_dir, filename) for filename in os.listdir(zip_dir) if filename.endswith(".zip")][0]
                args["processed"] = True
                args["import_path"] = zip_file_path
                self.uploader.perform_task(args)

        else:
            print("Please enter your image path properly \n\n\n\n\n")
            self.zip_upload()

    def get_args(self, func):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        return {arg: None for arg in arg_names}

    def perform_task(self, vars_args: dict):
        # if self.check_auth():
        if True:
            func = input("Choose your process:\n\
                         1. image upload \n\
                         2. Video upload\n\
                         3. gopro360max upload\n\
                         4. Advance options\n"
                         )

            if func == "1" or func == "image upload":
                self.perform_image_upload()

            elif func == "2" or func == "Video upload":
                self.perform_video_upload()

            elif func == "3" or func == "gopro360max upload":
                self.gopro360max_upload()

            elif func == "4" or func == "Advance options":
                advanced_func = input("Choose your advanced process:\n\
                                         4.1 Decompose \n\
                                         4.2 360 panorama image upload\n\
                                         4.3 Zip upload\n"
                                      )
                if advanced_func == "4.1" or advanced_func == "Decompose":
                    self.perform_decompose()
                if advanced_func == "4.2" or advanced_func == "360 panorama image upload":
                    self.panorama_image_upload()
                if advanced_func == "4.3" or advanced_func == "Zip upload":
                    self.zip_upload()
                elif advanced_func == "q":
                    exit()
            elif func == "q":
                exit()
            else:
                print("\n\nPlease enter a valid option\n\n")
                Run().perform_task(vars_args=None)


if __name__ == "__main__":
    print("Welcome to Mapilio-kit\n")
    Run().perform_task(vars_args=None)
