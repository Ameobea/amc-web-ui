cd frontend && yarn build
cd -
rm -rf backend/static
cp -r frontend/build backend/static
cd backend && python3 entrypoint.py
