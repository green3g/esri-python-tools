import lib.Geodatabase
import lib.Reproject_Tool import Reproject

def run_tool(from_db, to_db, projection):
    Geodatabase.clean(to_db)
    r = Reproject()
    r.reproject(from_db, to_db, projection)

#defaults if run at command line
if __name__ == '__main__':
    #defaul values
    from_db = 'N:/BaseData/faribault.gdb'
    to_db = 'C:/Data/projected_faribault.gdb'
    projection = 'N:/BaseData/rice_co.prj'

    #run the tool
    run_tool(from_db, to_db, projection)
