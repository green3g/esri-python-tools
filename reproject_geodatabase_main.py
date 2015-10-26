import lib.Geodatabase

def run_copy_tool(from_db, to_db, projection):
    Geodatabase.clean(to_db)
    Geodatabase.reproject(from_db, to_db, projection)

#defaults if run at command line
if __name__ == '__main__':
    #defaul values
    from_db = 'N:/BaseData/faribault.gdb'
    to_db = 'C:/Data/projected_faribault.gdb'
    projection = 'N:/BaseData/rice_co.prj'

    #run the tool
    run_copy_tool(from_db, to_db, projection)
