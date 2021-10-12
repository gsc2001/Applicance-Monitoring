import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Divider,
  useTheme,
  colors
} from '@material-ui/core';
import * as recharts from 'recharts';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';
import { useEffect, useState } from 'react';

const initialData = [
  {
    timestamp: new Date(),
    uv: 4000
  }
];

const Sales = (props) => {
  const theme = useTheme();
  const [data, setData] = useState(initialData);
  useEffect(() => {
    let id = 0;
    const interval = setInterval(() => {
      const newData = (oldData) => {
        console.log(oldData);
        return [
          ...oldData,
          {
            name: `temp${id}`,
            timestamp: new Date(),
            uv: Math.random() * 2000 + 1000
          }
        ];
      };
      setData(newData);
      id += 1;
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const formatDate = (d) => {
    return `${d.getMinutes()}:${d.getSeconds()}`;
  };
  return (
    <Card {...props}>
      <CardHeader title="Current Flowing" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 400,
            position: 'relative'
          }}
        >
          {/* <Bar
            data={data}
            options={options}
          /> */}
          <recharts.LineChart width={500} height={300} data={data}>
            <recharts.XAxis dataKey="timestamp" tickFormatter={formatDate} />
            <recharts.YAxis />
            <recharts.Tooltip />
            <recharts.CartesianGrid stroke="#eee" strokeDasharray="5 5" />
            <recharts.Line type="monotone" dataKey="uv" stroke="#8884d8" />
            <recharts.Line type="monotone" dataKey="pv" stroke="#82ca9d" />
          </recharts.LineChart>
        </Box>
      </CardContent>
      <Divider />
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'flex-end',
          p: 2
        }}
      >
        <Button
          color="primary"
          endIcon={<ArrowRightIcon />}
          size="small"
          variant="text"
        >
          Overview
        </Button>
      </Box>
    </Card>
  );
};

export default Sales;
