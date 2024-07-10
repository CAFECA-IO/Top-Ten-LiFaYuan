from app import app
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Quart app.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Quart app on.')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=True)
