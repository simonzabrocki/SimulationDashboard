import sys,os
IPYNB_FILENAME = 'report.ipynb'
CONFIG_FILENAME = '.config_ipynb'

def main(argv):
    with open(CONFIG_FILENAME,'w') as f:
        f.write(' '.join(argv))
    os.system('jupyter nbconvert --execute {:s} --to html  --output-dir="./outputs/reports/" --no-input --template classic'.format(IPYNB_FILENAME))
    return None

if __name__ == '__main__':
    main(sys.argv)