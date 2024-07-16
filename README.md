
# Mapilary web app

This project is a web application that fetches images from the Mapillary API using specified bounding box coordinates and presents them on a map. It includes functionality for users to retrieve images from a designated area through a button interface. The project is implemented using Redis for caching with Flask and utilizes multithreaded programming techniques.

![image](https://github.com/user-attachments/assets/dcee528d-648a-4569-8738-7aa93d60baaf)


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)


markdown
Copy code
## Installation

1. Clone this repository to your local machine:

   ```bash 
   git clone https://github.com/maichaouat/MapWebsite.git
2. Navigate into the project directory:

    ```bash
    cd app
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the Flask application using:
    ```bash
    python main.py

5. Access the application in your web browser at http://localhost:5000.

## Pulling the Docker Image
If you prefer to use the Docker image directly from Docker Hub, follow these steps:

Open your terminal or command prompt.

Pull the Docker image from Docker Hub using the following command:

    docker pull maiu51/mapliaryapp:latest
  

Once the image is downloaded, you can run it using:
    docker run -p 5000:5000 maiu51/mapliaryapp:latest

Access the application in your web browser at http://localhost:5000.
## Usage

1. Access the application in your web browser.
2. Use the map interface to navigate to the desired location.
3. Click on the "Retrieve Points from Part-3" button to fetch images from the specified area.

## Dependencies

- Flask
- requests
- configurations
- Flask-Caching

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on [GitHub](https://github.com/maichaouat/MapWebsite).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Copy and paste this content into your README file on GitHub. Adjust the GitHub repository URL (`https://github.com/maichaouat/MapWebsite.git`) as needed.
