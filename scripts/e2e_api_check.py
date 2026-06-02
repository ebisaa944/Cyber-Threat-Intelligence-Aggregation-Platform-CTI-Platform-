import requests, sys

def main():
    base='http://127.0.0.1:8000/api/'
    s=requests.Session()
    print('=== REGISTER ===')
    try:
        r=s.post(base+'auth/register/',json={'username':'e2euser2','password':'TestPass123','email':'e2e2@example.com'},timeout=10)
        print(r.status_code, r.text)
    except Exception as e:
        print('register failed', e); sys.exit(1)
    print('\n=== TOKEN ===')
    try:
        r=s.post(base+'auth/token/',json={'username':'e2euser2','password':'TestPass123'},timeout=10)
        print(r.status_code, r.text)
        j=r.json()
        access=j.get('access')
        if not access:
            print('no access token'); sys.exit(1)
    except Exception as e:
        print('token failed', e); sys.exit(1)
    headers={'Authorization':f'Bearer {access}'}
    print('\n=== CREATE REPORT ===')
    try:
        r=s.post(base+'reports/',json={'title':'E2E Report','summary':'Summary from E2E'},headers=headers,timeout=10)
        print(r.status_code, r.text)
        created = r.json()
        rid = created.get('id')
    except Exception as e:
        print('create report failed', e); rid=None

    print('\n=== LIST REPORTS ===')
    try:
        r=s.get(base+'reports/',headers=headers,timeout=10)
        print(r.status_code, r.text[:800])
    except Exception as e:
        print('list reports failed', e)

    print('\n=== FETCH THREATS ===')
    try:
        r=s.get(base+'threats/',headers=headers,timeout=10)
        print(r.status_code, (r.text or '')[:800])
    except Exception as e:
        print('threats failed', e)

    print('\n=== FETCH CVES ===')
    try:
        r=s.get(base+'cves/',headers=headers,timeout=10)
        print(r.status_code, (r.text or '')[:800])
    except Exception as e:
        print('cves failed', e)

    print('\n=== FETCH SUMMARY ===')
    try:
        r=s.get(base+'summary/',headers=headers,timeout=10)
        print(r.status_code, r.text)
    except Exception as e:
        print('summary failed', e)

    if rid:
        print('\n=== DOWNLOAD REPORT ===')
        try:
            r=s.get(base+f'reports/{rid}/download_pdf/',headers=headers,timeout=20)
            print('download status', r.status_code, 'content-type', r.headers.get('content-type'))
        except Exception as e:
            print('download failed', e)

    print('\nE2E script completed')

if __name__ == '__main__':
    main()
